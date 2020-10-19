"""This module shows some very basic examples of how to use fixtures in pytest-helm-charts.
"""
import logging
from typing import Dict

import pykube

from pytest_helm_charts.fixtures import Cluster

from pytest_helm_charts.giantswarm_app_platform.app import AppFactoryFunc, ConfiguredApp
import time

logger = logging.getLogger(__name__)


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


def test_app(kube_cluster: Cluster, app_factory: AppFactoryFunc, cluster_type: str, chart_extra_info: Dict[str, str]) -> None:
    """Example shows how you can access additional information about the cluster the tests are running on"""
    logger.info(f"Running on cluster type {cluster_type}")

    config_values: YamlDict = {
        # "replicaCount": replicas,
        # "ingress": {
        #     "enabled": "true",
        #     "annotations": {"kubernetes.io/ingress.class": "nginx"},
        #     "paths": ["/"],
        #     "hosts": [host_url],
        # },
        # "autoscaling": {"enabled": "false"},
    }

    api = kube_cluster.kube_client

    # create namespace
    namespace_name = "efk-stack-app-test2"
    try:
        ns = pykube.Namespace.objects(api).get(name=namespace_name)
        # FIXME .get_or_none()
    except pykube.exceptions.ObjectDoesNotExist:
        obj = {
            "apiVersion": "v1",
            "kind": "Namespace",
            "metadata": {
                "name": namespace_name,
            },
        }
        pykube.Namespace(api, obj).create()

    # app = app_factory(
    #     "efk-stack-app",
    #     "0.3.2-19bb12f72fd3cf2ec9e95130cf2496f5c81b537a",
    #     namespace_name,
    #     "http://chart-museum.giantswarm.svc:8080/charts",
    #     namespace_name,
    #     config_values,
    # )

    # wait for deployment
    # time.sleep(600)


    print("waiting for client")
    while True:
        r = pykube.Deployment.objects(api, namespace=namespace_name).get_or_none(name="efk-stack-app-opendistro-es-client")
        try:
            if r and r.obj["status"]["readyReplicas"] > 0:
                break
        except:
            pass
        print(".", end="")
        time.sleep(10)
    print("client ready")
    # print(r.obj)

    print("waiting for master")
    while True:
        r = pykube.StatefulSet.objects(api, namespace=namespace_name).get_or_none(name="efk-stack-app-opendistro-es-master")
        try:
            if r and r.obj["status"]["readyReplicas"] > 0:
                break
        except:
            pass
        print(".", end="")
        time.sleep(10)
    print("master ready")
    # print(r.obj)
