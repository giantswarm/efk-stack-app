import pytest

# from .cluster import Cluster
from pytest_kube import Cluster

from functools import partial


@pytest.fixture(scope="session")
def cluster_create(request):
    keep = request.config.getoption("keep_cluster")
    cluster = None

    def _cluster_create(request, cluster_cls: Cluster, *args, **kwargs):
        """Provide a Kubernetes kind cluster as test fixture"""
        # FIXME maybe allow a configurable prefix here instead?
        # name = request.config.getoption("cluster_name")

        nonlocal cluster

        if not cluster:
            cluster = cluster_cls(kwargs.pop("name"))
            cluster.create(*args, **kwargs)

        return cluster

    yield partial(_cluster_create, request)
    if not keep:
        cluster.delete()
