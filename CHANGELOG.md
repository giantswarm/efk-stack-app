# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project's packages adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2020-12-08

### Changed

- Opendistro for Elasticsearch
  - Update to `Elasticsearch` and `Kibana` version `7.9.1`. For more details see [Open Distro for Elasticsearch 1.11.0 Release Notes](https://github.com/opendistro-for-elasticsearch/opendistro-build/blob/master/release-notes/opendistro-for-elasticsearch-release-notes-1.11.0.md)
  - Merged [upstream chart](https://github.com/opendistro-for-elasticsearch/opendistro-build/tree/master/helm) changes
  - Changes to [schema value files](https://helm.sh/docs/topics/charts/#schema-files):
    - Moved opendistro-es specific schema to sub chart
    - Allow `null` for `podDisruptionBudget` fields so it is possible to [overwrite unwanted defaults](https://helm.sh/docs/chart_template_guide/values_files/#deleting-a-default-key)
    - Removed verification for `config` sections for now

### Added

FIXME
- Simple default `readinessProbe` for Elasticsearch: Just checks for TCP connection

## [0.3.5] - 2020-11-25

### Fixed

- corrected es-client service name in es-client-ingress. ([#36](https://github.com/giantswarm/efk-stack-app/pull/36))

## [0.3.4] - 2020-10-30

### Added

- enabled antiAffinity to spread `master`, `data` and `client` nodes across `hostname`s
- enabled PDBs for `master` and `data`: `minAvailable=66%` and for `client`: `minavailable=1`
- builds are now automatically tested with functional testing

## [0.3.3] - 2020-10-22

### Changed

- Set `es-client` URI to a static value to avoid issues when templating across multiple subcharts. ([#24](https://github.com/giantswarm/efk-stack-app/pull/24))

## [0.3.2] - 2020-09-15

### Changed

- Reverted label selector changes originally added in [#10](https://github.com/giantswarm/efk-stack-app/pull/10) to not block upgrades ([#20](https://github.com/giantswarm/efk-stack-app/pull/20))

## [0.3.1] - 2020-09-11

### Added

- Giant Swarm monitoring annotations and labels.

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

[Unreleased]: https://github.com/giantswarm/efk-stack-app/compare/v0.3.5...HEAD
[0.3.5]: https://github.com/giantswarm/efk-stack-app/compare/v0.3.4...v0.3.5
[0.3.4]: https://github.com/giantswarm/efk-stack-app/compare/v0.3.3...v0.3.4
[0.3.3]: https://github.com/giantswarm/efk-stack-app/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/giantswarm/efk-stack-app/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/giantswarm/efk-stack-app/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/giantswarm/efk-stack-app/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/giantswarm/efk-stack-app/compare/v0.1.5...v0.2.0
[0.1.5]: https://github.com/giantswarm/efk-stack-app/compare/v0.1.4..v0.1.5
[0.1.4]: https://github.com/giantswarm/efk-stack-app/compare/v0.1.3..v0.1.4
[0.1.3]: https://github.com/giantswarm/efk-stack-app/releases/tag/v0.1.3
