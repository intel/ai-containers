# Text Generation Inference on Intel GPU

A Rust, Python and gRPC server for text generation inference by huggingface on Intel GPUs.

For more information about how to use Huggingface text-generation-inference with Intel optimizations, check out [huggingface's documentation](https://huggingface.co/docs/text-generation-inference/installation_intel).

> [!TIP]
> For Gaudi-related documentation, check out [tgi-gaudi](https://github.com/huggingface/tgi-gaudi).

![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 1.16.0](https://img.shields.io/badge/AppVersion-1.16.0-informational?style=flat-square)

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| deploy.configMapName | string | `"intel-proxy-config"` | ConfigMap of Environment Variables |
| deploy.image | string | `"ghcr.io/huggingface/text-generation-inference:latest-intel"` | Intel TGI Image |
| deploy.model | string | `"HuggingFaceTB/SmolLM-135M"` | Model to be loaded |
| deploy.quantize | string | `""` | Enable Quantization (ex: bitsandbytes-nf4) |
| deploy.replicaCount | int | `1` | Number of pods |
| deploy.resources | object | `{"limits":{"cpu":"4000m","gpu.intel.com/i915":1},"requests":{"cpu":"1000m","memory":"1Gi"}}` | Resource configuration |
| deploy.resources.limits."gpu.intel.com/i915" | int | `1` | Intel GPU Device Configuration |
| fullnameOverride | string | `""` | Full qualified Domain Name |
| ingress | object | `{"annotations":{},"className":"","enabled":false,"hosts":[{"host":"chart-example.local","paths":[{"path":"/","pathType":"ImplementationSpecific"}]}],"tls":[]}` | Ingress configuration |
| nameOverride | string | `""` | Name of the serving service |
| service | object | `{"port":80,"type":"NodePort"}` | Service configuration |
