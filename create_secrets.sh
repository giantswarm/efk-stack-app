#!/bin/bash

kubectl create ns opendistro2

kubectl create secret generic kibana-auth --from-literal=username='admin' --from-literal=password='admin'  --from-literal=cookie='akrjp45dpluix6vlbbivdv3e0w03fkichp29llkr' -n opendistro2

kubectl create secret generic elasticsearch-transport-certs -n opendistro2 \
      --from-file=elk-transport-crt.pem=./out/transport.crt \
      --from-file=elk-transport-key.pem=./out/transport.pem \
      --from-file=elk-transport-root-ca.pem=./out/root.crt

kubectl create secret generic -n opendistro2 elasticsearch-security-config --from-file=configs/config.yml