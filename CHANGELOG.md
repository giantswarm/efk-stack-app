# 0.1.3
- First release

# 0.1.4
- Retagged images
- Created changelog
- Fixed manual deploy script

# 0.1.5
- Ignore efk-stack-app namespace in fluentd

# 0.2.0
## Opendistro
- Upgrade to OpenDistro 1.6.0 [Changelog](https://github.com/opendistro-for-elasticsearch/opendistro-build/blob/master/release-notes/release-notes-odfe-1.6.0.md)
- Add pod affinity
- Allow subpath for Persistent Volumes
- Allow use of unmanaged Persistent Volumes
- Configurable init images

## FluentD
- Upgrade fluentD version to 3.0.0
- Get auth from secret

## ElasticSearch Exporter
- Get auth info from secret
- `prometheusRule.rules` are now processed as Helm template, allowing to set variables in them. This means that if a rule contains a {{ $value }}, Helm will try replacing it and probably fail.

## ElasticSearch Curator
- Get auth info from secret