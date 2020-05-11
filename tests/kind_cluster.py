from pathlib import Path

from pytest_kind import KindCluster as KindClusterUpstream

from .cluster import Cluster

# based on https://github.com/hjacobs/pytest-kind/blob/master/pytest_kind/cluster.py
# but uses different __init__ from Cluster

class KindCluster(Cluster):
    super().__init__()

    self.kind_path = Path("/usr/local/bin/kind")

    def create(self, *args, **kwargs):
        """Creates the cluster"""
        # FIXME what if cluster exists?
        return KindCluster.create(self, *args, **kwargs)
