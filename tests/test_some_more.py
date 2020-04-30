import subprocess
import logging
from pathlib import Path
from tempfile import NamedTemporaryFile
import random

import yaml
import requests
from pykube import Pod
import pytest

from functools import partial
import time


# @pytest.fixture(scope="session")
# def kind_cluster_create(request):
#     # keep = request.config.getoption("keep_cluster")
#     cluster = None

#     def _kind_cluster_create(request, config_file = None):
#         """Provide a Kubernetes kind cluster as test fixture"""
#         nonlocal cluster
#         name = request.config.getoption("cluster_name")
#         cluster = KindCluster(name)
#         cluster.create(config_file)
#         return cluster

#     yield partial(_kind_cluster_create, request)
#     if not keep:
#         # name = request.config.getoption("cluster_name")
#         # cluster = KindCluster(name)
#         cluster.delete()


def test_kubernetes_version(kind_cluster):
    assert kind_cluster.api.version == ('1', '17')


def test_kubernetes_chart_museum(kind_cluster):
    kind_cluster.kubectl("apply", "-f", Path(__file__).parent / "chart-museum.yaml")
    kind_cluster.kubectl("-n", "giantswarm", "rollout", "status", "deployment/chart-museum")
    # TODO
    assert kind_cluster.api.version == ('1', '17')


def test_helm(kind_cluster):
    assert "The Kubernetes package manager" in subprocess.check_output(
        ["helm", "--help"],
        encoding="utf-8"
    )


def test_efk_stack_charts(kind_cluster):
    assert "The Kubernetes package manager" in subprocess.check_output(
        ["helm", "--help"],
        encoding="utf-8"
    )

    chart_path = Path(".") / "helm" / "efk-stack-app"
    subprocess.check_output(
        ["helm", "template", "helm-test-efk", chart_path],
        encoding="utf-8"
    )

    with NamedTemporaryFile(mode="w+") as tmp:
        rendered_manifests = subprocess.check_output(
            ["helm", "template", "helm-test-efk", chart_path], 
            encoding="utf-8"
        )

        resources = list(yaml.safe_load_all(rendered_manifests))
        yaml.dump_all(documents=resources, stream=tmp)
        kind_cluster.kubectl("apply", "-f", tmp.name)

    # breakpoint()

    namespace = "default"

    kind_cluster.kubectl("-n", namespace, "rollout", "status", "statefulset/helm-test-efk-opendistro-es-master")
    kind_cluster.kubectl("-n", namespace, "rollout", "status", "statefulset/helm-test-efk-opendistro-es-data")
    kind_cluster.kubectl("-n", namespace, "rollout", "status", "deployment/helm-test-efk-opendistro-es-kibana")
    

    all_masters_initialized = False

    while not all_masters_initialized:
        all_masters_initialized = True
        
        for pod in Pod.objects(kind_cluster.api).filter(selector="statefulset.kubernetes.io/pod-name=helm-test-efk-opendistro-es-master-0"):
            # assert "Node 'helm-test-efk-opendistro-es-master-0' initialized" in pod.logs()   
            if not "Node 'helm-test-efk-opendistro-es-master-0' initialized" in pod.logs():
                all_masters_initialized = False
                time.sleep(2)


    with kind_cluster.port_forward("service/helm-test-efk-opendistro-es-client-service", 9200) as port:
        r = requests.get(f"http://localhost:{port}/", auth=('admin', 'admin'))

        r.raise_for_status()
        assert "You Know, for Search" in r.text


def test_elasticsearch_unauthorized(kind_cluster):

    with kind_cluster.port_forward("service/helm-test-efk-opendistro-es-client-service", 9200) as port:
        r = requests.get(f"http://localhost:{port}/")

        with pytest.raises(requests.exceptions.HTTPError):
            r.raise_for_status()

        assert r.status_code == 401
