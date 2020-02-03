#!/bin/bash

kubectl create ns opendistro2

helm template --namespace opendistro2 --name opendistro --tiller-namespace giantswarm ./helm/opendistro-app > deploy.yaml

kubectl apply -f deploy.yaml