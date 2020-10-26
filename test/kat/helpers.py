from typing import List

import pykube
from pykube import HTTPClient
from pytest_helm_charts.utils import wait_for_namespaced_objects_condition, wait_for_jobs_to_complete


def _statefulset_ready(s: pykube.StatefulSet) -> bool:
    complete = "readyReplicas" in s.obj["status"] and s.replicas == int(s.obj["status"]["readyReplicas"])
    return complete


def wait_for_stateful_sets_to_run(
    kube_client: HTTPClient,
    stateful_set_names: List[str],
    stateful_sets_namespace: str,
    timeout_sec: int,
    missing_ok: bool = False,
) -> List[pykube.StatefulSet]:
    return wait_for_namespaced_objects_condition(
        kube_client,
        pykube.StatefulSet,
        stateful_set_names,
        stateful_sets_namespace,
        _statefulset_ready,
        timeout_sec,
        missing_ok=missing_ok,
    )


def make_job(
    kube_client: pykube.HTTPClient,
    name_prefix: str,
    namespace: str,
    command: List[str],
    image: str = "quay.io/giantswarm/busybox:1.32.0",
    restart_policy: str = "OnFailure",
) -> pykube.Job:
    return pykube.Job(
        kube_client,
        {
            "apiVersion": "batch/v1",
            "kind": "Job",
            "metadata": {"generateName": name_prefix, "namespace": namespace},
            "spec": {
                "template": {
                    "spec": {
                        "containers": [
                            {
                                "name": f"{name_prefix}job",
                                "image": image,
                                "command": command,
                            }
                        ],
                        "restartPolicy": restart_policy,
                    },
                },
            },
        },
    )


def run_job_to_completion(
    kube_client: pykube.HTTPClient,
    name_prefix: str,
    namespace: str,
    command: List[str],
    timeout_sec: int = 60,
    missing_ok: bool = False,
    image: str = "quay.io/giantswarm/busybox:1.32.0",
    restart_policy: str = "OnFailure",
) -> pykube.Job:
    job = make_job(kube_client, name_prefix, namespace, command, image=image, restart_policy=restart_policy)
    job.create()

    wait_for_jobs_to_complete(
        kube_client,
        [job.name],
        namespace,
        timeout_sec,
        missing_ok=missing_ok,
    )

    return job


def ensure_namespace_exists(kube_client: pykube.HTTPClient, namespace_name: str) -> pykube.Namespace:
    try:
        pykube.Namespace.objects(kube_client).get(name=namespace_name)
    except pykube.exceptions.ObjectDoesNotExist:
        obj = {
            "apiVersion": "v1",
            "kind": "Namespace",
            "metadata": {
                "name": namespace_name,
            },
        }
        ns = pykube.Namespace(kube_client, obj)
        ns.create()
        return ns
