# to be implemented
# maybe via multipass?
# https://medium.com/better-programming/local-k3s-cluster-made-easy-with-multipass-108bf6ce577c

# better: running K3d (K3s in Docker)
# https://rancher.com/docs/k3s/latest/en/advanced/#running-k3d-k3s-in-docker-and-docker-compose


# root@x1-yoga:/pytest# ./k3d-linux-amd64 create cluster
# INFO[0000] Created network 'k3d-k3s-default'
# INFO[0000] Created volume 'k3d-k3s-default-images'
# INFO[0001] Creating node 'k3d-k3s-default-master-0'
# INFO[0002] Pulling image 'docker.io/rancher/k3s:v1.17.4-k3s1'
# INFO[0013] Creating LoadBalancer 'k3d-k3s-default-masterlb'
# INFO[0015] Pulling image 'docker.io/iwilltry42/k3d-proxy:v0.0.1'
# INFO[0020] Cluster 'k3s-default' created successfully!
# INFO[0020] You can now use it like this:
# export KUBECONFIG=$(./k3d-linux-amd64 get kubeconfig k3s-default)
# kubectl cluster-info

from .cluster import Cluster


class K3dCluster(Cluster):
    pass
