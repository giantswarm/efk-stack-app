from pathlib import Path
from typing import Union

import pykube

from .cluster import Cluster


class ExistingCluster(Cluster):
    # def __init__

    def __create(self, name, kubeconfig_path: Union[str, Path] = None):

        self.name = name
        config = pykube.KubeConfig.from_file(self.kubeconfig_path)
        self.api = pykube.HTTPClient(config)

    # not implemented
    def load_docker_image(self, docker_image: str):
        pass

    # does not apply
    def delete(self):
        pass
