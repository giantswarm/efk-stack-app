#!/bin/bash

kubectl create ns efk-stack-app

helm template --namespace efk-stack-app --name efk-stack-app ./helm/efk-stack-app -f example_values/ingress_enabled_aws.yaml --kube-version 1.16 > deploy.yaml

kubectl apply -f deploy.yaml -n efk-stack-app