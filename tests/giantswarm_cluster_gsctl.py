import json
import logging
import subprocess
import time
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Union

import yaml

import pykube

from .cluster import Cluster

# @dataclass
# class GiantswarmClusterConfig:


# FIXME rename to GiantswarmClusterLegacy
# or GiantswarmClusterGsctl


class GiantswarmClusterGsctl(Cluster):
    def __init__(
        self,
        name,
        endpoint,
        email,
        password,
        config=None,
        config_file: Union[str, Path] = None,
        # *args,
    ):
        super().__init__(name)

        self.gsctl_path = Path("/usr/local/bin/gsctl")
        self.endpoint = endpoint
        self.email = email
        self.password = password
        self.owner = "giantswarm"
        self.id = None
        self.config = config

        if not config_file:
            self.config_file = "-"
        else:
            self.config_file = config_file
            # FIXME better read in config_file here to self.config
            # and get rid off self.config_file

        self.api = self.__create()

    def __create(self):
        """Create the cluster if it does not exist (otherwise re-use)"""

        login_cmd = f"""
            gsctl login {self.email}
                --endpoint={self.endpoint}
                --password={self.password}
        """
        # out = subprocess.check_output(login_cmd.split(), encoding="utf-8")
        subprocess.run(login_cmd.split(), encoding="utf-8", check=True)

        list_cmd = f"""
            gsctl list clusters
                --output=json
        """
        out = subprocess.check_output(list_cmd.split(), encoding="utf-8")

        cluster_exists = False
        # FIXME should check for self.id
        if json.loads(out):
            for cluster in json.loads(out):
                if cluster["name"] == self.name:
                    cluster_exists = True

        if not cluster_exists:
            logging.info(f"Creating cluster {self.name}..")

            # with NamedTemporaryFile(mode="w+") as tmp:
            #     # breakpoint()
            #     yaml.dump(self.config, tmp)

            #     # resources = list(yaml.safe_load_all(rendered_manifests))
            #     # yaml.dump_all(documents=resources, stream=tmp)
            #     # kind_cluster.kubectl("apply", "-f", tmp.name)

            create_cmd = f"""
                gsctl create cluster
                    --name={self.name}
                    --owner={self.owner}
                    --file={self.config_file}
            """
            # breakpoint()
            subprocess.run(
                create_cmd.split(), input=yaml.dump(self.config), encoding="utf-8", check=True
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
        return pykube.HTTPClient(config)

    # not implemented
    def load_docker_image(self, docker_image: str):
        pass

    def delete(self):
        """Delete the cluster"""
        logging.info(f"Deleting cluster {self.name}..")
        subprocess.run(["gsctl", "delete", "cluster", "--force", self.id], check=True)
