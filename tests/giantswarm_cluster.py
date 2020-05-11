import json
import logging
import subprocess
import time
from pathlib import Path
from typing import Union

import yaml

import pykube

from .cluster import Cluster

# @dataclass
# class GiantswarmClusterConfig:


class GiantswarmCluster(Cluster):

    # FIXME
    # Refactor, see cluster.py

    def create(
        self,
        name,
        endpoint,
        email,
        password,
        config=None,
        config_file: Union[str, Path] = None,
    ):
        """Create the cluster if it does not exist (otherwise re-use)"""

        self.name = name
        self.endpoint = endpoint
        self.email = email
        self.password = password
        self.owner = "giantswarm"
        self.id = None
        self.config = config
        if not config_file:
            config_file = "-"

        login_cmd = f"""
            gsctl login {self.email}
                --endpoint={self.endpoint}
                --password={self.password}
        """
        out = subprocess.check_output(login_cmd.split(), encoding="utf-8")

        list_cmd = f"""
            gsctl list clusters
                --output=json
        """
        out = subprocess.check_output(list_cmd.split(), encoding="utf-8")

        cluster_exists = False

        if json.loads(out):
            for cluster in json.loads(out):
                if cluster["name"] == self.name:
                    cluster_exists = True

        if not cluster_exists:
            logging.info(f"Creating cluster {self.name}..")

            create_cmd = f"""
                gsctl create cluster
                    --name={self.name}
                    --owner={self.owner}
                    --file={config_file}
            """
            subprocess.run(
                create_cmd.split(), stdin=yaml.safe_load(self.config), check=True
            )
            cluster_exists = True

        out = subprocess.check_output(list_cmd.split(), encoding="utf-8")

        for cluster in json.loads(out):
            if cluster["name"] == self.name:
                self.id = cluster["id"]

        kubeconfig_cmd = f"""
            gsctl create kubeconfig
                --ttl=1h
                --certificate-organizations=system:masters
                --cluster={self.id}
                --description=pytest
                --self-contained={self.kubeconfig_path}
                --force
        """
        subprocess.run(kubeconfig_cmd.split(), encoding="utf-8", check=True)

        cluster_ready = False
        while not cluster_ready:
            cp = subprocess.run(
                [
                    self.kubectl_path,
                    f"--kubeconfig={self.kubeconfig_path}",
                    "cluster-info",
                ]
            )
            if not cp.returncode:
                cluster_ready = True
            else:
                time.sleep(2)

        config = pykube.KubeConfig.from_file(self.kubeconfig_path)
        self.api = pykube.HTTPClient(config)

    # not implemented
    def load_docker_image(self, docker_image: str):
        pass

    def delete(self):
        """Delete the cluster"""
        logging.info(f"Deleting cluster {self.name}..")
        subprocess.run(["gsctl", "delete", "cluster", "--force", self.id], check=True)
