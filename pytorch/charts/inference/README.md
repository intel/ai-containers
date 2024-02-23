# TorchServe

![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 1.16.0](https://img.shields.io/badge/AppVersion-1.16.0-informational?style=flat-square)

A Helm chart for Kubernetes

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| deploy.image | string | `"pytorch/torchserve:latest-cpu"` |  |
| deploy.models | string | `"all"` | `<name>=<filename>` space separated list of models to register on startup |
| deploy.modelConfig | string | `"/home/model-server/config.properties"` | Path to model server config file |
| deploy.replicas | string | `1` |  |
| deploy.resources.limits.cpu | string | `32` |  |
| deploy.resources.limits.memory | string | `"16Gi"` |  |
| deploy.resources.requests.cpu | string | `"1000m"` |  |
| deploy.resources.requests.memory | string | `"512Mi"` |  |
| deploy.storage.nfs.path | string | `"nil"` |  |
| deploy.storage.nfs.readOnly | bool | `true` |  |
| deploy.storage.nfs.server | string | `"nil"` |  |
| deploy.storage.nfs.subPath | string | `"nil"` |  |
| name | string | `"ipex-serving"` |  |
| service.type | string | `"NodePort"` | Service Type (NodePort or LoadBalancer) |

>**Note:** AKS/EKS/GKS will distribute external IPs such that only a `LoadBalancer` is required, but on-prem clusters will by default require an ingress to distribute an external ip, so by default the service is created as a `NodePort` type so that any Node IP can be used to access the TorchServe API
