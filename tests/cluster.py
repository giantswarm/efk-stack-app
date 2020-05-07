import random
import socket
import subprocess
import time
from contextlib import contextmanager
from pytest_kind import KindCluster
from typing import Generator, Union

class Cluster(KindCluster):
    def __init__(self):
        pass

#     def create(self, config_file: Union[str, Path] = None):
#         """Create the cluster if it does not exist (otherwise re-use)"""
#         pass

#     def load_docker_image(self, docker_image: str):
#         pass

    def kubectl(self, *args: str, **kwargs) -> str:
        """Run a kubectl command against the cluster and return the output as string"""
        # self.ensure_kubectl()
        return subprocess.check_output(
            ["kubectl", *args],
            # env={"KUBECONFIG": str(self.kubeconfig_path)},
            encoding="utf-8",
            **kwargs,
        )

    @contextmanager
    def port_forward(
        self,
        service_or_pod_name: str,
        remote_port: int,
        *args,
        local_port: int = None,
        retries: int = 10,
    ) -> Generator[int, None, None]:
        """Run "kubectl port-forward" for the given service/pod and use a random local port"""
        port_to_use: int
        proc = None
        for i in range(retries):
            if proc:
                proc.kill()
            # Linux epheremal port range starts at 32k
            port_to_use = local_port or random.randrange(5000, 30000)
            proc = subprocess.Popen(
                [
                    "kubectl",
                    "port-forward",
                    service_or_pod_name,
                    f"{port_to_use}:{remote_port}",
                    *args,
                ],
                # env={"KUBECONFIG": str(self.kubeconfig_path)},
            )
            time.sleep(1)
            returncode = proc.poll()
            if returncode is not None:
                if i >= retries - 1:
                    raise Exception(
                        f"kubectl port-forward returned exit code {returncode}"
                    )
                else:
                    # try again
                    continue
            s = socket.socket()
            try:
                s.connect(("127.0.0.1", port_to_use))
            except:
                if i >= retries - 1:
                    raise
            finally:
                s.close()
        try:
            yield port_to_use
        finally:
            if proc:
                proc.kill()

#     def delete(self):
#         pass
