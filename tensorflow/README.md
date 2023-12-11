# TensorFlow Ingredients

## TensorFlow

### Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| BASE_IMAGE_NAME | `ubuntu` | Base Operating System |
| BASE_IMAGE_TAG | `22.04` | Base Operating System Version |
| IDP_VERSION | `core` | Intel Distribution of Python version(either `full` or `core`) |
| MINICONDA_VERSION | `latest-Linux-x86_64` | Miniconda Version from `https://repo.anaconda.com/miniconda` |
| PACKAGE_OPTION | `pip` | Stock Python (pypi) or Intel Python (conda) (`pip` or `idp`) |
| PYTHON_VERSION | `3.10` | Python Version |
| TF_PACKAGE | `intel-tensorflow` | TF Package (`tensorflow`, `intel-tensorflow`, `intel-tensorflow-avx512`) |
| TF_PACKAGE_VERSION | `2.14.0` | TensorFlow Version |

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
| HOROVOD_VERSION | `0.28.0` | Horovod Version |
| INC_VERSION | `2.1.1` | Neural Compressor Version |
| MPI | `openmpi` | MPI Installation type (`openmpi` or `mpich`) |

### ITEX XPU Base

Built from Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| ICD_VER | `23.17.26241.33-647~22.04` | OpenCL Version |
| LEVEL_ZERO_GPU_VER | `1.3.26241.33-647~22.04` | Level Zero GPU Version |
| LEVEL_ZERO_VER | `1.11.0-647~22.04` | Level Zero Version |
| DPCPP_VER | `2023.2.1-16` | DPCPP Version | 
| MKL Version | `2023.2.0-49495` | MKL Version |
| CCL_VER | `2021.10.0-49084` | CCL Version |
| TF_VERSION | `2.13` | TensorFlow Version |

### ITEX XPU Jupyter

Built from ITEX XPU Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| PORT | `8888` | Server UI Port |

#### Distributed Training on k8s

Use _N_-Nodes in your Training with MPI Operator and an optimized production container.

##### Distributed Production Container

Create a Distributed Production Container using Intel Optimized TensorFlow MultiNode layers. For Example:

```dockerfile
# Add Some Multinode image layers
FROM intel/intel-optimized-tensorflow:2.12.0-pip-openmpi-multinode as prod-base
# Use an existing container target
FROM base as prod

# Copy in Intel Optimized TensorFlow MultiNode python environment, this will overwrite any packages with the same name
COPY --from=prod-base /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.10/dist-packages
COPY --from=prod-base /usr/local/bin /usr/local/bin

# Install MPI
RUN apt-get update -y && apt-get install -y --no-install-recommends --fix-missing \
    libopenmpi-dev \
    openmpi-bin \
    openmpi-common \
    openssh-client \
    openssh-server
...
```

##### Build the Container with New Stage

For a BKM on how to install MPI see the [MLOps Best Known Method](Dockerfile#L128).

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

Configure the Helm Chart by changing [mpijob](chart/templates/mpijob.yaml#L28), [pvc](chart/templates/pvc.yaml), and [values](chart/values.yaml) files.

Afterwards, deploy to the cluster with `helm install`. To see all of the options, see the [README](chart/README.md) for the chart.

```bash
export NAMESPACE=kubeflow
helm install ---namespace ${NAMESPACE} \
     --set metadata.name=<workflow-name> \
     --set metadata.namespace=<namespace with training operator> \
     --set imageName=<Docker Image repository/Name> \
     --set imageTag=<Docker Image Tag> \
     --set slotsPerWorker=1 \
     ...
     itex-distributed
     charts/training
```

To see an existing configuration utilizing this method, check out [Intel® Transfer Learning Tool](https://github.com/IntelAI/transfer-learning/blob/main/docker/README.md#kubernetes)'s implementation.

##### Troubleshooting

- [Common Horovod Issues](https://horovod.readthedocs.io/en/stable/troubleshooting_include.html)
- [MPI Operator Reference](https://github.com/kubeflow/mpi-operator)
- [Training Operator Reference](https://github.com/kubeflow/training-operator)
- When applying proxies specify all of your proxies in a configmap in the same namespace, and add the following to both your launcher and workers:

```yaml
envFrom:
  - configMapRef:
      name: my-proxy-configmap-name
```

## TensorFlow Serving

### TF Serving

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| BASE_IMAGE_NAME | `ubuntu` | Base Operating System |
| BASE_IMAGE_TAG | `22.04` | Base Operating System Version |
| BAZEL_VERSION | `5.4.0` | Bazel Version |
| TF_PACKAGE | `intel-tensorflow` | TF Package (`tensorflow`, `intel-tensorflow`, `intel-tensorflow-avx512`) |
| TF_SERVING_BAZEL_OPTIONS | `'--local_ram_resources=HOST_RAM*0.8 --local_cpu_resources=HOST_CPUS-4'` | Bazel Options |
| TF_SERVING_BUILD_OPTIONS | `'--config=mkl --config=release --define=build_with_openmp=false --copt=-march=native'` | Serving Build Options |
| TF_SERVING_VERSION | `2.12.0` | TensorFlow Version |
| TF_SERVING_VERSION_GIT_BRANCH | `${TF_SERVING_VERSION}` | Branch/Ref for TF Serving Repository |

### Serving MKL

Built from TF Serving

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| BASE_IMAGE_NAME | `${TF_PACKAGE:-intel-tensorflow}-${BASE_IMAGE_NAME:-ubuntu}-${PACKAGE_OPTION:-pip}` | TF Serving Name |
| BASE_IMAGE_TAG | `serving` | TF Serving Tag |
| TF_SERVING_BUILD | `${BASE_IMAGE_NAME:-ubuntu}:${BASE_IMAGE_TAG:-22.04}` | Serving MKL OS `Base:Tag` |
| TF_SERVING_VERSION_GIT_COMMIT | `${TF_SERVING_VERSION}` | Commit/Branch/Ref for TF Serving Repository |
