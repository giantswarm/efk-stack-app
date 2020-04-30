# pytest

Also see:
- https://github.com/giantswarm/pytest-kube
- https://github.com/giantswarm/kube-app-testing
- https://github.com/hjacobs/pytest-kind
- https://codeberg.org/hjacobs/kube-web-view/src/branch/master/tests/e2e
- https://github.com/giantswarm/gs-in-kind


```bash
# create docker image from https://github.com/giantswarm/pytest-kube

docker run -ti \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --network host \
  -v $PWD:/pytest \
  local/pytest-kube
```


```bash
kind create cluster
kubectl apply -f ./chart-museum.yaml
```

helm template
kubectl apply

or

app-cr

---

```bash
# --keep-cluster

```


---

docker build -t local/kind-in-docker ./tests/docker

docker run -ti \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --network host \
  -v $PWD:/pytest \
  local/kind-in-docker \
    python -m pytest --keep-cluster



export KUBECONFIG=".pytest-kind/pytest-kind/kind-config-pytest-kind"

helm template ching ./helm/efk-stack-app | kubectl apply -f -


set -x KUBECONFIG "$HOME/.kube/config.d/pytest-kind.config" \
  && kind get kubeconfig --name pytest-kind > $KUBECONFIG

  