# IPEX Distributed

![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 1.16.0](https://img.shields.io/badge/AppVersion-1.16.0-informational?style=flat-square)

A Helm chart for Kubernetes

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| imageName | string | `"intel/intel-optimized-pytorch"` |  |
| imageTag | string | `"2.0.0-pip-multinode"` |  |
| masterResources.cpu | int | `32` | Number of Compute for Master |
| masterResources.memory | string | `"16Gi"` | Amount of Memory for Master |
| metadata.name | string | `"ipex-distributed"` |  |
| metadata.namespace | string | `"kubeflow"` |  |
| pvcName | string | `"ipex"` |  |
| pvcResources | string | `"2Gi"` | Amount of shared storage for workers and launcher |
| pvcScn | string | `"nil"` | PVC `StorageClassName` |
| workerResources.cpu | int | `32` | Number of Compute per Worker |
| workerResources.memory | string | `"16Gi"` | Amount of Memory per Worker |
| workers | int | `4` | Number of Workers |
