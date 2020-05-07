import random
import socket
import subprocess
import time
from contextlib import contextmanager
from pytest_kind import KindCluster
from typing import Generator, Union

from pathlib import Path

class Cluster(KindCluster):
    def __init__(self, name: str):
        self.name = name

        path = Path(".pytest-kind")
        self.path = path / name
        self.path.mkdir(parents=True, exist_ok=True)

        self.kind_path = Path("/usr/local/bin/kind")
        self.kubectl_path = Path("/usr/local/bin/kubectl")
        self.kubeconfig_path = self.path / f"kind-config-{self.name}"
