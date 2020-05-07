import pytest

from .cluster import Cluster
from functools import partial


@pytest.fixture(scope="session")
def cluster_create(request):
    keep = request.config.getoption("keep_cluster")
    cluster = None

    def _cluster_create(request, cluster_cls, *args, **kwargs):
        """Provide a Kubernetes kind cluster as test fixture"""
        # name = request.config.getoption("cluster_name")
        nonlocal cluster
        cluster = cluster_cls(kwargs["name"])
        cluster.create(*args, **kwargs)
        # cluster.create()
        return cluster

    yield partial(_cluster_create, request)
    if not keep:
        cluster.delete()

