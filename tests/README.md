# pytest

> ** Highly experimantal - not followin best practices yet - just jumpstarting **


To run the tests set `version: 0.1.0` in `/helm/efk-stack-app/Chart.yaml`. Then create a docker image from [giantswarm/pytest-kube](https://github.com/giantswarm/pytest-kube). And run the following from the root of this repository:

```bash
# create docker image from https://github.com/giantswarm/pytest-kube

docker run -ti \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --network host \
  -v $PWD:/pytest \
  local/pytest-kube \
    python -m pytest --keep-cluster
```
Leave out `--keep-cluster` if you want the cluster to be destroyed after the test run.

To inspect the kind cluster during the test you could run `kind` outside of the cluster something like this:

```bash
export KUBECONFIG="$HOME/.kube/config.d/pytest-kind.config" \
  && kind get kubeconfig --name pytest-kind > $KUBECONFIG

kubectl get -A pods
```

See also:
- https://github.com/giantswarm/pytest-kube
- https://github.com/giantswarm/kube-app-testing
- https://github.com/hjacobs/pytest-kind
- https://codeberg.org/hjacobs/kube-web-view/src/branch/master/tests/e2e
- https://github.com/giantswarm/gs-in-kind
