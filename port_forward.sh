#!/bin/bash

POD=$(kubectl get pod -n opendistro -l app=opendistro-opendistro-es-kibana -o jsonpath="{.items[0].metadata.name}")

kubectl port-forward $POD 5601:5601 -n opendistro