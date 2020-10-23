from typing import List

import pykube
from pykube import HTTPClient
from pytest_helm_charts.utils import wait_for_namespaced_objects_condition


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
