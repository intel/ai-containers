# PyTorch Ingredients

## PyTorch

### Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| BASE_IMAGE_NAME | `ubuntu` | Base Operating System |
| BASE_IMAGE_TAG | `22.04` | Base Operating System Version |
| IDP_VERSION | `core` | Intel Distribution of Python version(either `full` or `core`) |
| IPEX_VERSION | `2.1.0` | Intel Extension for PyTorch Version |
| MINICONDA_VERSION | `latest-Linux-x86_64` | Miniconda Version from `https://repo.anaconda.com/miniconda` |
| PACKAGE_OPTION | `pip` | Stock Python (pypi) or Intel Python (conda) (`pip` or `idp`) |
| PYTHON_VERSION | `3.10` | Python Version |
| PYTORCH_VERSION | `2.1.0+cpu` | PyTorch Version |
| TORCHAUDIO_VERSION | `2.1.0+cpu` | TorchAudio Version |
| TORCHVISION_VERSION | `0.16.0+cpu` | TorchVision Version |

### Jupyter

Built from Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| PORT | `8888` | Server UI Port |

### MLFlow

Built from Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| PORT | `5000` | Server UI Port |

### MultiNode

Built from Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| INC_VERSION | `2.3.1` | Neural Compressor Version |
| ONECCL_VERSION | `2.1.0+cpu` | TorchCCL Version |

### IPEX XPU Base

Built from Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| ICD_VER | `23.17.26241.33-647~22.04` | OpenCL Version |
| LEVEL_ZERO_GPU_VER | `1.3.26241.33-647~22.04` | Level Zero GPU Version |
| LEVEL_ZERO_VER | `1.11.0-647~22.04` | Level Zero Version |
| DPCPP_VER | `2023.2.1-16` | DPCPP Version | 
| MKL Version | `2023.2.0-49495` | MKL Version |
| CCL_VER | `2021.10.0-49084` | CCL Version |
| TORCH_VERSION | `2.0.1a0+cxx11.abi` | Torch Version |
| TORCHVISION_VERSION | `0.15.2a0+cxx11.abi` | Torchvision Version |
| IPEX_VERSION | `2.0.110+xpu` | IPEX Version |
| TORCH_WHL_URL | `https://developer.intel.com/ipex-whl-stable-xpu` | Wheel URL |
| ONECCL_BIND_PT_VERSION | `2.0.100` | TorchCCL Version | 

### IPEX XPU Jupyter

Built from IPEX XPU Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| PORT | `8888` | Server UI Port |

### IPEX Prod

Create python environment using a compile stage. Expose REST and gRPC ports. Install Java and Python. Create model-server user and create necessary directories. Create entrypoint file and add torchserve config file.

| Component | Package Manager |
| --- | --- |
| captum | pip |
| cython | pip |
| intel_extension_for_pytorch | pip |
| openjdk-17-jdk | apt |
| pynvml | pip |
| python3 | apt |
| pyyaml | pip |
| torch | pip |
| torch-model-archiver | pip |
| torch-workflow-archiver | pip |
| torchaudio | pip |
| torchserve | pip |
| torchtext | pip |
| torchvision | pip |

#### Distributed Training on k8s

Use _N_-Nodes in your Training with PyTorchJobs and Kubeflow's Training Operator with an optimized production container.

##### Distributed Production Container

Create a Distributed Production Container using Intel Optimized PyTorch MultiNode layers. For Example:

```dockerfile
# Add Some Multinode image layers
FROM intel/intel-optimized-pytorch:2.1.0-pip-multinode as prod-base
# Use an existing container target
FROM base as prod

# Copy in Intel Optimized PyTorch MultiNode python environment, this will overwrite any packages with the same name
COPY --from=prod-base /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.10/dist-packages
COPY --from=prod-base /usr/local/bin /usr/local/bin

...
```

##### Build the Container with New Stage

```bash
docker build ... --target prod -t my_container:prod .
```

##### Configure Kubernetes

Using an existing Kubernetes Cluster of any flavor, install the standalone training operator from GitHub or use a pre-existing Kubeflow configuration.

```bash
kubectl apply -k "github.com/kubeflow/training-operator/manifests/overlays/standalone"
```

Ensure that the training operator deployment readiness status `1/1` before proceeding.

##### Deploy Distributed Job

Install [Helm](https://helm.sh/docs/intro/install/)

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 && \
chmod 700 get_helm.sh && \
./get_helm.sh
```

Configure the Helm Chart by changing [pytorchjob](chart/templates/pytorchjob.yaml#L18-L46), [pvc](chart/templates/pvc.yaml), and [values](chart/values.yaml) files.

Afterwards, deploy to the cluster with `helm install`. To see all of the options, see the [README](chart/README.md) for the chart.

```bash
export NAMESPACE=kubeflow
helm install ---namespace ${NAMESPACE} \
     --set metadata.name=<workflow-name> \
     --set metadata.namespace=<namespace with training operator> \
     --set imageName=<Docker Image repository/Name> \
     --set imageTag=<Docker Image Tag> \
     ...
     ipex-distributed
     charts/training
```

To see an existing configuration utilizing this method, check out [Intel® Extension for Transformers](https://github.com/intel/intel-extension-for-transformers/blob/main/docker/README.md#kubernetes)' implementation.

##### Troubleshooting

- [TorchCCL Reference](https://github.com/intel/torch-ccl)
- [PyTorchJob Reference](https://www.kubeflow.org/docs/components/training/pytorch/)
- [Training Operator Reference](https://github.com/kubeflow/training-operator)
- When applying proxies specify all of your proxies in a configmap in the same namespace, and add the following to both your launcher and workers:

```yaml
envFrom:
  - configMapRef:
      name: my-proxy-configmap-name
```
