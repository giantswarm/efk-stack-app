# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project's packages adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2020-09-04

### Added

- Add release workflow

### Changed

- Helm Charts are based now on the [official repository](https://github.com/opendistro-for-elasticsearch/opendistro-build/tree/master/helm)
- OpenDistro is upgraded to [`1.8.0`](https://github.com/opendistro-for-elasticsearch/opendistro-build/blob/master/release-notes/opendistro-for-elasticsearch-release-notes-1.8.0.md)
- Split image strings into separate values to allow for overriding of registry by chart-operator ([#15](https://github.com/giantswarm/efk-stack-app/pull/15))
- OpenDistro is upgraded to [`1.9.0`](https://github.com/opendistro-for-elasticsearch/opendistro-build/blob/master/release-notes/opendistro-for-elasticsearch-release-notes-1.9.0.md) ([#16](https://github.com/giantswarm/efk-stack-app/pull/16))

## [0.2.0] 2020-04-15
### Opendistro
- Upgrade to OpenDistro 1.6.0 [Changelog](https://github.com/opendistro-for-elasticsearch/opendistro-build/blob/master/release-notes/release-notes-odfe-1.6.0.md)
- Add pod affinity
- Allow subpath for Persistent Volumes
- Allow use of unmanaged Persistent Volumes
- Configurable init images

### FluentD
- Upgrade fluentD version to 3.0.0
- Get auth from secret

### ElasticSearch Exporter
- Get auth info from secret
- `prometheusRule.rules` are now processed as Helm template, allowing to set variables in them. This means that if a rule contains a {{ $value }}, Helm will try replacing it and probably fail.

### ElasticSearch Curator
- Get auth info from secret

## [0.1.5] 2020-02-19
- Ignore efk-stack-app namespace in fluentd

## [0.1.4] 2020-02-19
- Retagged images
- Created changelog
- Fixed manual deploy script

## [0.1.3] 2020-02-10
- First release

[Unreleased]: https://github.com/giantswarm/efk-stack-app/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/giantswarm/efk-stack-app/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/giantswarm/efk-stack-app/compare/v0.1.5...v0.2.0
[0.1.5]: https://github.com/giantswarm/efk-stack-app/compare/v0.1.4..v0.1.5
[0.1.4]: https://github.com/giantswarm/efk-stack-app/compare/v0.1.3..v0.1.4
[0.1.3]: https://github.com/giantswarm/efk-stack-app/releases/tag/v0.1.3
