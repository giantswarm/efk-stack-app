#!/bin/bash

kubectl create ns opendistro

kubectl create secret generic kibana-auth --from-literal=username='admin' --from-literal=password='admin'  --from-literal=cookie='akrjp45dpluix6vlbbivdv3e0w03fkichp29llkr' -n opendistro

kubectl create secret generic elasticsearch-admin-certs -n opendistro \
      --from-file=admin-crt.pem=./certs/admin.pem \
      --from-file=admin-key.pem=./certs/admin-key.pem \
      --from-file=admin-root-ca.pem=./certs/admin-root-ca.pem

kubectl create secret generic elasticsearch-transport-certs -n opendistro \
      --from-file=elk-transport-crt.pem=./certs/elk-transport.pem \
      --from-file=elk-transport-key.pem=./certs/elk-transport-key.pem \
      --from-file=elk-transport-root-ca.pem=./certs/elk-transport-root-ca.pem

kubectl create secret generic elasticsearch-rest-certs -n opendistro \
      --from-file=elk-rest-crt.pem=./certs/rest.pem \
      --from-file=elk-rest-key.pem=./certs/rest-key.pem \
      --from-file=elk-rest-root-ca.pem=./certs/rest-root-ca.pem

kubectl create secret generic elasticsearch-kibana-certs -n opendistro \
      --from-file=kibana-crt.pem=./certs/kibana.pem \
      --from-file=kibana-key.pem=./certs/kibana-key.pem \
      --from-file=kibana-root-ca.pem=./certs/kibana-root-ca.pem

kubectl create secret generic -n opendistro elasticsearch-security-config --from-file=config.yml