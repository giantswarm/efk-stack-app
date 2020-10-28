"""This module shows some very basic examples of how to use fixtures in pytest-helm-charts.
"""
import datetime
import logging
from contextlib import contextmanager
from typing import Dict, List, Optional

import pykube
import pytest
from pytest_helm_charts.fixtures import Cluster

from helpers import wait_for_stateful_sets_to_run, run_job_to_completion, ensure_namespace_exists

logger = logging.getLogger(__name__)

app_name = "efk-stack-app"
client_service_base_url = "http://admin:admin@opendistro-es-client-service:9200"
namespace_name = "default"
catalog_name = "chartmuseum"

timeout: int = 360


@contextmanager
def delete_logs_scope(kube_cluster: Cluster):
    yield
    delete_logs(kube_cluster.kube_client)


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


# scope "module" means this is run only once, for the first test case requesting! It might be tricky
# if you want to assert this multiple times
@pytest.fixture(scope="module")
def efk_stateful_sets(kube_cluster: Cluster) -> List[pykube.StatefulSet]:
    return wait_for_efk_stateful_sets(kube_cluster)


def wait_for_efk_stateful_sets(kube_cluster: Cluster) -> List[pykube.StatefulSet]:
    stateful_sets = wait_for_stateful_sets_to_run(
        kube_cluster.kube_client,
        [f"{app_name}-opendistro-es-data", f"{app_name}-opendistro-es-master"],
        namespace_name,
        timeout,
    )
    return stateful_sets


def test_pods_available(kube_cluster: Cluster, efk_stateful_sets: List[pykube.StatefulSet]):
    for s in efk_stateful_sets:
        assert int(s.obj["status"]["readyReplicas"]) > 0


def test_masters_green(kube_cluster: Cluster, efk_stateful_sets: List[pykube.StatefulSet]):
    masters = [s for s in efk_stateful_sets if s.name == f"{app_name}-opendistro-es-master"]
    assert len(masters) == 1

    run_job_to_completion(
        kube_cluster.kube_client,
        "check-efk-green-",
        namespace_name,
        [
            "sh",
            "-c",
            "wget -O - -q " f"{client_service_base_url}/_cat/health" " | grep green",
        ],
        timeout_sec=timeout,
    )


def generate_logs(
    kube_client: pykube.HTTPClient, logs_namespace: str, range_start: int = 1, range_end: int = 100
) -> pykube.Job:
    gen_job = run_job_to_completion(
        kube_client,
        "generate-logs-",
        logs_namespace,
        [
            "sh",
            "-c",
            f'seq {range_start} {range_end} | xargs printf "generating-logs-ding-dong-%03d\n"',
        ],
        timeout_sec=timeout,
        restart_policy="Never",
        backoffLimit=0,
    )
    flush_index(kube_client)
    return gen_job


def run_shell_against_efk(
    kube_client: pykube.HTTPClient, pod_name_prefix: str, namespace: str, command: str
) -> pykube.Job:
    return run_job_to_completion(
        kube_client,
        pod_name_prefix,
        namespace,
        [
            "sh",
            "-c",
            command,
        ],
        image="docker.io/giantswarm/tiny-tools:3.10",
        timeout_sec=timeout,
    )


def query_logs(kube_client: pykube.HTTPClient, expected_no_log_entries_lower_bound: int) -> pykube.Job:
    command = (
        f"curl -s '{client_service_base_url}/_search?q=ding-dong&size=1000' "  # query more than we're expecting
        f"| jq --exit-status '.hits.total.value >= {expected_no_log_entries_lower_bound}'"
    )
    return run_shell_against_efk(kube_client, "query-logs-", namespace_name, command)


def flush_index(kube_client: pykube.HTTPClient) -> pykube.Job:
    command = f"curl '{client_service_base_url}/_flush'"
    return run_shell_against_efk(kube_client, "flush-index-", namespace_name, command)


def delete_logs(kube_client: pykube.HTTPClient, index_date: Optional[datetime.datetime] = None) -> pykube.Job:
    # FIXME: This index name generation will work only for data generated on the same single day!
    # Better way to do it is to check index names by running
    # curl -s 'http://admin:admin@127.0.0.1:9200/_search?q=ding-dong&size=1000' | jq '[.hits.hits[]._index] | unique'
    fluentd_index_date = index_date if index_date is not None else datetime.datetime.now()
    index_name = f"fluentd-{fluentd_index_date.strftime('%Y.%m.%d')}"
    command = f"curl -XDELETE '{client_service_base_url}/{index_name}'"
    return run_shell_against_efk(kube_client, "delete-logs-", namespace_name, command)


@pytest.mark.usefixtures("efk_stateful_sets")
def test_logs_are_picked_up(kube_cluster: Cluster) -> None:
    # create a new namespace
    # fluentd is configured to ignore certain namespaces
    logs_ns_name = "logs-ns"
    ensure_namespace_exists(kube_cluster.kube_client, logs_ns_name)

    with delete_logs_scope(kube_cluster):
        generate_logs(kube_cluster.kube_client, logs_ns_name)
        query_logs(kube_cluster.kube_client, expected_no_log_entries_lower_bound=100)


@pytest.mark.usefixtures("efk_stateful_sets")
def test_can_survive_pod_restart(kube_cluster: Cluster, efk_stateful_sets: List[pykube.StatefulSet]) -> None:
    logs_ns_name = "logs-ns"
    ensure_namespace_exists(kube_cluster.kube_client, logs_ns_name)

    with delete_logs_scope(kube_cluster):
        generate_logs(kube_cluster.kube_client, logs_ns_name)
        query_logs(kube_cluster.kube_client, expected_no_log_entries_lower_bound=100)

        # find 1st pod of each of the core stateful sets, then delete it
        pods_to_delete = []
        for sts in efk_stateful_sets:
            pod_selector = sts.obj["spec"]["selector"]
            pods = pykube.Pod.objects(kube_cluster.kube_client).filter(
                namespace=namespace_name,
                selector=pod_selector["matchLabels"],
            )
            pods_to_delete.append(pykube.Pod(kube_cluster.kube_client, pods.response["items"][0]))
        for pod in pods_to_delete:
            pod.delete()

        # wait for pods to get back up
        wait_for_efk_stateful_sets(kube_cluster)

        # assert again
        generate_logs(kube_cluster.kube_client, logs_ns_name, range_start=101, range_end=200)
        query_logs(kube_cluster.kube_client, 200)


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
