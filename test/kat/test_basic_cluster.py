"""This module shows some very basic examples of how to use fixtures in pytest-helm-charts.
"""
import logging
from typing import Dict, List

import pykube
import pytest

from pytest_helm_charts.fixtures import Cluster
from pytest_helm_charts.utils import wait_for_namespaced_objects_condition

logger = logging.getLogger(__name__)

app_name = "efk-stack-app"
namespace_name = "default"
catalog_name = "chartmuseum"

timeout: int = 90


def test_api_working(kube_cluster: Cluster) -> None:
    """Very minimalistic example of using the [kube_cluster](pytest_helm_charts.fixtures.kube_cluster)
    fixture to get an instance of [Cluster](pytest_helm_charts.clusters.Cluster) under test
    and access its [kube_client](pytest_helm_charts.clusters.Cluster.kube_client) property
    to get access to Kubernetes API of cluster under test.
    Please refer to [pykube](https://pykube.readthedocs.io/en/latest/api/pykube.html) to get docs
    for [HTTPClient](https://pykube.readthedocs.io/en/latest/api/pykube.html#pykube.http.HTTPClient).
    """
    assert kube_cluster.kube_client is not None
    assert len(pykube.Node.objects(kube_cluster.kube_client)) >= 1


def test_cluster_info(kube_cluster: Cluster, cluster_type: str, chart_extra_info: Dict[str, str]) -> None:
    """Example shows how you can access additional information about the cluster the tests are running on"""
    logger.info(f"Running on cluster type {cluster_type}")
    key = "external_cluster_type"
    if key in chart_extra_info:
        logger.info(f"{key} is {chart_extra_info[key]}")
    assert kube_cluster.kube_client is not None
    assert cluster_type != ""


def _statefulset_ready(s: pykube.StatefulSet) -> bool:
    complete = "readyReplicas" in s.obj["status"] and s.replicas == int(s.obj["status"]["readyReplicas"])
    return complete


@pytest.fixture(scope="function")
def stateful_sets(kube_cluster: Cluster) -> List[pykube.StatefulSet]:
    return wait_for_namespaced_objects_condition(
        kube_cluster.kube_client,
        pykube.StatefulSet,
        [f"{app_name}-opendistro-es-data", f"{app_name}-opendistro-es-master"],
        namespace_name,
        _statefulset_ready,
        timeout,
        missing_ok=False,
    )


def test_pods_available(kube_cluster: Cluster, stateful_sets: List[pykube.StatefulSet]):
    for s in stateful_sets:
        assert int(s.obj["status"]["readyReplicas"]) > 0


def test_masters_green(kube_cluster: Cluster, stateful_sets: List[pykube.StatefulSet]):
    masters = [s for s in stateful_sets if s.name == f"{app_name}-opendistro-es-master"]
    assert len(masters) == 1

    pod = pykube.Pod(
        kube_cluster.kube_client,
        {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {"name": "check-green", "namespace": namespace_name},
            "spec": {
                "containers": [
                    {
                        "name": "query-health-endpoint",
                        "image": "quay.io/giantswarm/busybox:1.32.0",
                        "command": [
                            "sh",
                            "-c",
                            f"wget -O - -q http://admin:admin@{app_name}-opendistro-es-client-service:9200/_cat/health",
                        ],
                    }
                ],
                "restartPolicy": "OnFailure",
            },
        },
    )
    pod.create()

    wait_for_namespaced_objects_condition(
        kube_cluster.kube_client,
        pykube.Pod,
        [pod.name],
        namespace_name,
        (
            lambda pod: (
                "status" in pod.obj
                and "conditions" in pod.obj["status"]
                and len(pod.obj["status"]["conditions"]) > 0
                and "reason" in pod.obj["status"]["conditions"][0]
                and pod.obj["status"]["conditions"][0]["reason"] == "PodCompleted"
                and pod.obj["status"]["conditions"][0]["status"] == "True"
            )
        ),
        timeout,
        missing_ok=False,
    )

    logs = pod.logs()

    assert "green" in logs
    assert "100.0%" in logs

    # cleanup
    pod.delete()


# def make_app_cr(kube_client: pykube.HTTPClient, chart_version: str) -> None:
#     cr_name = f"{app_name}-test"
#     app: YamlDict = {
#         "apiVersion": "application.giantswarm.io/v1alpha1",
#         "kind": "App",
#         "metadata": {
#             "name": cr_name, "namespace": "giantswarm",
#             "labels": {"app": cr_name, "app-operator.giantswarm.io/version": "0.0.0"},
#         },
#         "spec": {
#             "catalog": catalog_name,
#             "version": chart_version,
#             "kubeConfig": {"inCluster": True},
#             "name": app_name,
#             "namespace": namespace_name,
#         },
#     }

#     return AppCR(kube_client, app)

# def test_app(kube_cluster: Cluster, cluster_type: str, chart_extra_info: Dict[str, str], chart_version: str) -> None:
#     """Example shows how you can access additional information about the cluster the tests are running on"""
#     logger.info(f"Running on cluster type {cluster_type}")


#     logger.info(f"Running on cluster type {chart_version}")

#     config_values: YamlDict = {
#         # "replicaCount": replicas,
#         # "ingress": {
#         #     "enabled": "true",
#         #     "annotations": {"kubernetes.io/ingress.class": "nginx"},
#         #     "paths": ["/"],
#         #     "hosts": [host_url],
#         # },
#         # "autoscaling": {"enabled": "false"},
#     }

#     api = kube_cluster.kube_client

#     # create namespace
#     try:
#         ns = pykube.Namespace.objects(api).get(name=namespace_name)
#         # FIXME .get_or_none()
#     except pykube.exceptions.ObjectDoesNotExist:
#         obj = {
#             "apiVersion": "v1",
#             "kind": "Namespace",
#             "metadata": {
#                 "name": namespace_name,
#             },
#         }
#         pykube.Namespace(api, obj).create()

#     app = make_app_cr(api, chart_version)
#     app.create()

#     # app = app_factory(
#     #     "efk-stack-app",
#     #     "0.3.2-19bb12f72fd3cf2ec9e95130cf2496f5c81b537a",
#     #     "chartmuseum",
#     #     "http://chart-museum.giantswarm.svc:8080/charts",
#     #     namespace_name,
#     #     config_values,
#     # )

#     # wait for deployment
#     # time.sleep(600)


#     logger.info("Waiting for elasticsearch client pods")
#     while True:
#         r = pykube.Deployment.objects(api, namespace=namespace_name)
#           .get_or_none(name="efk-stack-app-opendistro-es-client")
#         try:
#             if r and r.obj["status"]["readyReplicas"] > 0:
#                 break
#         except:
#             pass
#         # print(".", end="")
#         time.sleep(10)
#     logger.info("Elasticsearch client pods available")
#     print("client ready")
#     # print(r.obj)

#     print("waiting for master")
#     while True:
#         r = pykube.StatefulSet.objects(api, namespace=namespace_name)
#           .get_or_none(name="efk-stack-app-opendistro-es-master")
#         try:
#             if r and r.obj["status"]["readyReplicas"] > 0:
#                 break
#         except:
#             pass
#         print(".", end="")
#         time.sleep(10)
#     print("master ready")
#     # print(r.obj)
