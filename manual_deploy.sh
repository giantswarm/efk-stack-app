#!/bin/bash

kubectl create ns opendistro

helm template --namespace opendistro --name opendistro --tiller-namespace giantswarm ./helm/opendistro-app > deploy.yaml

kubectl apply -f deploy.yaml