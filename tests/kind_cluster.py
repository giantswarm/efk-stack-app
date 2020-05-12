from pathlib import Path

from pytest_kind import KindCluster as KindClusterUpstream

from .cluster import Cluster

# based on https://github.com/hjacobs/pytest-kind/blob/master/pytest_kind/cluster.py
# but uses different __init__ from Cluster


class KindCluster(Cluster):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, name=kwargs.pop("name"), **kwargs)

        self.kind_path = Path("/usr/local/bin/kind")
        self.__create(*args, **kwargs)

    def __create(self, *args, **kwargs):
        """Creates the cluster"""
        # FIXME what if cluster exists?
        # FIXME should return pykube.HTTPClient or so.
        # at the moment it is set at self.api
        return KindClusterUpstream.create(self, *args, **kwargs)
