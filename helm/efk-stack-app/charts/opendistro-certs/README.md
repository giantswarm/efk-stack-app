# OpenDistro certificate generator

Generates CA needed to enable OpenDistro security pluguin with (certstrap)[https://github.com/square/certstrap].

The rootCA and the transport certificates will be stored in kubernetes secrets using a Job to create the initial certificates and a cronjob to constantly check that the certificates are present.

If you wish to renew certificates you just can delete the kubernetes secret and they will be generated again.

**Certificate renewal is not implemented**


# Values
```
enabled: true

image: quay.io/giantswarm/opendistro-certs
imageTag: v0.0.3

organization: Giant Swarm
expiration: "5 years"
```

- **organization** will be used to generate all certificates

- **expiration** is used to issue the date when the certificates will expire