import random
import socket
import subprocess
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Union

# from pytest_kind import KindCluster
from pytest_kind import KindCluster as KindClusterUpstream


class Cluster:
    """
    [DEVNOTES]
    Based on [hjacobs/pytest-kind](https://github.com/hjacobs/pytest-kind/blob/master/pytest_kind/cluster.py),
    but some changes on the method signatures with the following idea:
    - Cluster __init__ takes everything needed for the specific Kubernetes provider
    - Cluster will be created
    - Returns cluster object with `api` field set to `pykube.HTTPClient` for the running
      cluster
    - There are helper functions like `kubectl`, `port_forward` and probably some more
    - `ensure` function will probably removed? Because surprising side-effect.

    Other ideas:
    - Allow specification of api version for connecting to the Providers?
      For example version of kind binary or cloud api.
    - Same for kubectl, helm, etc. Allow request for specific version
    - Maybe makes functions asynchronously? Since there is long blocking waiting time 
      expected
    """

    def __init__(self, name: str, *args, **kwargs):
        self.name = name

        # FIXME not sure: could also be a temporary directory?
        self.path = Path(".pytest-kube")
        self.path.mkdir(parents=True, exist_ok=True)

        # FIXME maybe make this an optional paremeter for self.kubectl, etc.
        self.kubectl_path = Path("/usr/local/bin/kubectl")
        # FIXME needs to be unique
        self.kubeconfig_path = self.path / f"kind-config-{self.name}"

        # FIXME also create self.api here if possible
        # self.api = self.create()

        # waitfor cluster-provider
        # waitfor kubeconfig
        # waitfor api
        #
        # https://docs.python.org/3/library/asyncio-task.html
        # await asyncio.sleep(1)

    def __create(self):
        """Create cluster and return pykube.HTTPClient()"""
        pass

        # create at cluster-provider
        # get kubeconfig
        # wait for api
        # ^ could be async and seperate steps?

    # FIXME not sure about this. after __init__ there should be ready state
    # def exists(self):
    #     """Check if the cluster exists for on the providers api point of view"""
    #     pass

    # def ready(self):
    #     """Check if the Kubernetes api is answering fine"""
    #     pass

    # FIXME feature might be removed. needed for kubectl and port_forward at the moment
    def ensure_kind(self):
        pass

    # FIXME feature might be removed. needed for kubectl and port_forward at the moment
    def ensure_kubectl(self):
        pass

    # def kubectl(self, *args: str, **kwargs) -> str:
    #     """Run a kubectl command against the cluster and return the output as string"""
    #     return KindCluster.kubectl(self, *args, **kwargs)

    def kubectl(self, *args: str, **kwargs) -> str:
        """Run a kubectl command against the cluster and return the output as string"""
        return KindClusterUpstream.kubectl(self, *args, **kwargs)

    # def helm(self, *args: str, **kwargs) -> str:
    #     """Run a kubectl command against the cluster and return the output as string"""
    #     self.ensure_kubectl()
    #     return subprocess.check_output(
    #         [str(self.kubectl_path), *args],
    #         env={"KUBECONFIG": str(self.kubeconfig_path)},
    #         encoding="utf-8",
    #         **kwargs,
    #     )

    # def kustomize(self, *args: str, **kwargs) -> str:
    #     pass

    # @contextmanager
    def port_forward(self, *args, **kwargs) -> Generator[int, None, None]:
        """Run "kubectl port-forward" for the given service/pod and use a random local port"""
        return KindClusterUpstream.port_forward(self, *args, **kwargs)

    def delete(self, *args, **kwargs) -> Generator[int, None, None]:
        """Run "kubectl port-forward" for the given service/pod and use a random local port"""
        return KindClusterUpstream.delete(self, *args, **kwargs)
