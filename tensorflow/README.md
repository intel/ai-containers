# TensorFlow Ingredients

```mermaid
%%{init: {'theme': 'dark'}}%%
flowchart TB
  tfbase[tf-base]
  jupyter
  inc
  tfserving[tf-serving]
  servingmkl[serving-mkl]
```

## TensorFlow

### Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| BASE_IMAGE_NAME | `ubuntu` | Base Operating System |
| BASE_IMAGE_TAG | `22.04` | Base Operating System Version |
| MINICONDA_VERSION | `latest-Linux-x86_64` | Miniconda Version from `https://repo.anaconda.com/miniconda` |
| PACKAGE_OPTION | `pip` | Stock Python (pypi) or Intel Python (conda) (`pip` or `idp`) |
| PYTHON_VERSION | `3.10` | Python Version |
| TF_PACKAGE | `intel-tensorflow` | TF Package (`tensorflow`, `intel-tensorflow`, `intel-tensorflow-avx512`) |
| TF_PACKAGE_VERSION | `2.12.0` | TensorFlow Version |

### Jupyter

Built from Base

### MultiNode

Built from Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| HOROVOD_VERSION | `0.28.0` | Horovod Version |
| INC_VERSION | `2.1.1` | Neural Compressor Version |
| MPI | `openmpi` | MPI Installation type (`openmpi` or `mpich`) |

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
