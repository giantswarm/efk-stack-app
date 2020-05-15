# pytest


To run the tests set `version: 0.1.0` in `/helm/efk-stack-app/Chart.yaml` and run the following Docker container from the root of this repository:

```bash
docker run -ti \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --network host \
  -v $PWD:/pytest \
  quay.io/giantswarm/pytest-kube:0.1.1-5db8c5b30f2747c53b0e939452fa4e98fd0b596a \
    python -m pytest --keep-cluster
```
Leave out `--keep-cluster` if you want the cluster to be destroyed after the test run.


See also:
- https://github.com/giantswarm/pytest-kube
- https://github.com/giantswarm/kube-app-testing
- https://github.com/hjacobs/pytest-kind
- https://codeberg.org/hjacobs/kube-web-view/src/branch/master/tests/e2e
- https://github.com/giantswarm/gs-in-kind
