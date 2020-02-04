#!/bin/bash

kubectl create ns opendistro

helm template --namespace opendistro --name opendistro --tiller-namespace giantswarm ./helm/opendistro-app -f example_values/ingress_enabled.yaml > deploy.yaml

kubectl apply -f deploy.yaml