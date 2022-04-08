# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project's packages adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Make number of days consistent between Curator code and docs

## [0.7.3] - 2022-04-06

### Added

- Set team annotation in Chart.yaml for alert routing.

### Fixed

- Fix deprecated api version for rbac.

## [0.7.2] - 2021-12-16

### Fixed

- fixes circleCI resource_class for testing
- fixes skipped version
- fixes app-build-suite config to replace chart version on release
- fixes chart version
- fixes apiVersion for ingress resources to `networking.k8s.io/v1`/`networking.k8s.io/v1beta1` depending on cluster capabilities

## [0.7.1] - 2021-12-14

### Fixed

- Security fix for CVE-2021-44228, which affect the Log4j library used in opendistro.

## [0.7.0] - 2021-12-01

### Changed

- Print deleted files when cleaning leftover lock files on NFS storage.
- Remove duplicate service for elasticsearch ingest nodes.
- Increase log level for fluentd.
- Increase log level for curator.

### Fixed

- Fix incorrect internal service name for `efk-stack-app-opendistro-es-client-service`.
- Set elasticsearch master and data service type to `ClusterIP`.
- Set config files permissions to `0600`.

## [0.6.0] - 2021-10-15

### Changed

- Update fluentd-elasticsearch container image to 3.3.0

## [0.5.4] - 2021-06-25

### Fixed

- Work around a Helm issue when `null` is used in the default values file. This caused problems with upgrades in some scenarious.
- Add a configurable workaround to [clean up leftover lock files on NFS storage](https://github.com/giantswarm/efk-stack-app/blob/master/README.md#running-on-nfs).

## [0.5.3] - 2021-06-21

### Added

- Add overridability of the Kibana image registry to allow users to ues their own image (extra-plugins, etc.).

## [0.5.2] - 2021-05-14

### Fixed

- Revert upstream changes of deployment labels. Those caused conflicts on upgrading.

## [0.5.1] - 2021-04-27

### Changed

- Update to Open Distro for Elasticsearch 1.13.2. For more details see their [Release Notes](https://github.com/opendistro-for-elasticsearch/opendistro-build/blob/main/release-notes/opendistro-for-elasticsearch-release-notes-1.13.2.md).


## [0.5.0] - 2021-03-08

### Changed

- Update to `Elasticsearch` and `Kibana` version `7.10.2`. For more details see [Open Distro for Elasticsearch 1.13.1 Release Notes](https://github.com/opendistro-for-elasticsearch/opendistro-build/blob/main/release-notes/opendistro-for-elasticsearch-release-notes-1.13.1.md)

## [0.4.1] - 2021-01-21

### Fixed

- Revert change of ingress naming schema [#49](https://github.com/giantswarm/efk-stack-app/pull/49)

## [0.4.0] - 2021-01-21

### Changed

- Opendistro for Elasticsearch
  - Update to `Elasticsearch` and `Kibana` version `7.9.1`. For more details see [Open Distro for Elasticsearch 1.11.0 Release Notes](https://github.com/opendistro-for-elasticsearch/opendistro-build/blob/master/release-notes/opendistro-for-elasticsearch-release-notes-1.11.0.md)
  - Merged [upstream chart](https://github.com/opendistro-for-elasticsearch/opendistro-build/tree/master/helm) changes
  - Changes to [schema value files](https://helm.sh/docs/topics/charts/#schema-files):
    - Moved opendistro-es specific schema to sub chart
    - Allow `null` for `podDisruptionBudget` fields so it is possible to [overwrite unwanted defaults](https://helm.sh/docs/chart_template_guide/values_files/#deleting-a-default-key)
    - Removed verification for `config` sections for now

## [0.3.6] - 2021-01-18

### Fixed

- corrected es-client hostname ([#43](https://github.com/giantswarm/efk-stack-app/pull/43))

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
- Upgrade to OpenDistro 1.6.0 [Changelog](https://github.com/opendistro-for-elasticsearch/opendistro-build/blob/main/release-notes/opendistro-for-elasticsearch-release-notes-1.6.0.md)
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

[Unreleased]: https://github.com/giantswarm/efk-stack-app/compare/v0.7.3...HEAD
[0.7.3]: https://github.com/giantswarm/efk-stack-app/compare/v0.7.2...v0.7.3
[0.7.2]: https://github.com/giantswarm/efk-stack-app/compare/v0.7.1...v0.7.2
[0.7.1]: https://github.com/giantswarm/efk-stack-app/compare/v0.7.0...v0.7.1
[0.7.0]: https://github.com/giantswarm/efk-stack-app/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/giantswarm/efk-stack-app/compare/v0.5.4...v0.6.0
[0.5.4]: https://github.com/giantswarm/efk-stack-app/compare/v0.5.3...v0.5.4
[0.5.3]: https://github.com/giantswarm/efk-stack-app/compare/v0.5.2...v0.5.3
[0.5.2]: https://github.com/giantswarm/efk-stack-app/compare/v0.5.1...v0.5.2
[0.5.1]: https://github.com/giantswarm/efk-stack-app/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/giantswarm/efk-stack-app/compare/v0.4.1...v0.5.0
[0.4.1]: https://github.com/giantswarm/efk-stack-app/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/giantswarm/efk-stack-app/compare/v0.3.6...v0.4.0
[0.3.6]: https://github.com/giantswarm/efk-stack-app/compare/v0.3.5...v0.3.6
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
