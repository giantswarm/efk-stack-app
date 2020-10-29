# EFK example values
## kind
### Known issue
**vm.max_map_count is too low**
As kind runs as a docker container, workloads running in kind will inherit the `vm.max_map_count` settings of the host machine. Elasticsearch require a `vm.max_map_count` of at least `262144`.
A lower value will result in the following error message:
```
max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
```

To set the required `vm.max_map_count` run this command on the host machine:
```bash
sudo sysctl -w vm.max_map_count=262144
```