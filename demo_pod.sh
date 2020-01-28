#!/bin/bash

kubectl create ns hello-world
echo "
    apiVersion: apps/v1 
    kind: Deployment
    metadata:
      name: helloworld
      labels:
        app: helloworld
      namespace: hello-world
    spec:
      replicas: 2
      selector:
        matchLabels:
          app: helloworld
      template:
        metadata:
          labels:
            app: helloworld
        spec:
          securityContext:
            runAsUser: 1000
          containers:
          - name: helloworld
            image: giantswarm/helloworld:latest
            ports:
            - containerPort: 8080" | kubectl apply -f -