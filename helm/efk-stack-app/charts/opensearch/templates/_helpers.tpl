{{/* vim: set filetype=mustache: */}}
{{/*
Copyright 2019 Viasat, Inc.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at

    http://www.apache.org/licenses/LICENSE-2.0

or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.
*/}}

{{/*
Expand the name of the chart.
*/}}
{{- define "opensearch.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "opensearch.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}


{{/*
Define standard labels for frequently used metadata.
*/}}
{{- define "opensearch.labels.standard" -}}
app: {{ template "opensearch.fullname" . }}
chart: "{{ .Chart.Name }}-{{ .Chart.Version }}"
{{- end -}}

{{/*
Define labels for deployment/statefulset selectors.
We cannot have the chart label here as it will prevent upgrades.
*/}}
{{- define "opensearch.labels.selector" -}}
app: {{ template "opensearch.fullname" . }}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "opensearch.opensearch-dashboards.serviceAccountName" -}}
{{- if .Values.opensearch-dashboards.serviceAccount.create -}}
    {{ default (include "opensearch.fullname" .) .Values.opensearch-dashboards.serviceAccount.name }}-opensearch-dashboards
{{- else -}}
    {{ default "default" .Values.opensearch-dashboards.serviceAccount.name }}
{{- end -}}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "opensearch.opensearch.serviceAccountName" -}}
{{- if .Values.opensearch.serviceAccount.create -}}
    {{ default (include "opensearch.fullname" .) .Values.opensearch.serviceAccount.name }}-es
{{- else -}}
    {{ default "default" .Values.opensearch.serviceAccount.name }}
{{- end -}}
{{- end -}}

{{/*
Return the proper Docker Image Registry Secret Names
*/}}
{{- define "opensearch.imagePullSecrets" -}}
{{/*
Helm 2.11 supports the assignment of a value to a variable defined in a different scope,
but Helm 2.9 and 2.10 does not support it, so we need to implement this if-else logic.
Also, we can not use a single if because lazy evaluation is not an option
*/}}
{{- if .Values.global }}
{{- if .Values.global.imagePullSecrets }}
imagePullSecrets:
{{- range .Values.global.imagePullSecrets }}
  - name: {{ . }}
{{- end }}
{{- else if or .Values.opensearch-dashboards.imagePullSecrets .Values.opensearch.imagePullSecrets .Values.opensearch.initContainer.imagePullSecrets }}
imagePullSecrets:
{{- range .Values.opensearch-dashboards.imagePullSecrets }}
  - name: {{ . }}
{{- end }}
{{- range .Values.opensearch.imagePullSecrets }}
  - name: {{ . }}
{{- end }}
{{- range .Values.opensearch.initContainer.imagePullSecrets }}
  - name: {{ . }}
{{- end }}
{{- end -}}
{{- else if or .Values.opensearch-dashboards.imagePullSecrets .Values.opensearch.imagePullSecrets .Values.opensearch.initContainer.imagePullSecrets }}
imagePullSecrets:
{{- range .Values.opensearch-dashboards.imagePullSecrets }}
  - name: {{ . }}
{{- end }}
{{- range .Values.opensearch.imagePullSecrets }}
  - name: {{ . }}
{{- end }}
{{- range .Values.opensearch.initContainer.imagePullSecrets }}
  - name: {{ . }}
{{- end }}
{{- end -}}
{{- end -}}

{{- define "master-nodes" -}}
{{- template "opensearch.fullname" . -}}-master
{{- end -}}

{{- define "initial-master-nodes" -}}
{{- $replicas := .Values.opensearch.master.replicas | int }}
  {{- range $i, $e := untilStep 0 $replicas 1 -}}
    {{ template "master-nodes" $ }}-{{ $i }},
  {{- end -}}
{{- end -}}
