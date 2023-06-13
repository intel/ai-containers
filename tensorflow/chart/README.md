# ITEX Distributed

![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 1.16.0](https://img.shields.io/badge/AppVersion-1.16.0-informational?style=flat-square)

A Helm chart for Kubernetes

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| imageName | string | `"intel/intel-optimized-tensorflow"` |  |
| imageTag | string | `"2.12.0-pip-openmpi-multinode"` |  |
| metadata.name | string | `"itex-distributed"` |  |
| metadata.namespace | string | `"kubeflow"` |  |
| pvcName | string | `"itex"` |  |
| pvcResources | string | `"2Gi"` | Amount of shared storage for workers and launcher |
| pvcScn | string | `"nil"` | PVC `StorageClassName` |
| resources.cpu | int | `2` | Number of Compute for Launcher |
| resources.memory | string | `"4Gi"` | Amount of Memory for Launcher |
| slotsPerWorker | int | `1` | Number of Processes per Worker |
| workerResources.cpu | int | `4` | Number of Compute per Worker |
| workerResources.memory | string | `"8Gi"` | Amount of Memory per Worker |
| workers | int | `4` | Number of Workers |
