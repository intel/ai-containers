## Build and Test TensorFlow Ingredient Containers

### Project structure:
```
├── Makefile
├── README.md
├── base
│   ├── Dockerfile.debian.pip
│   ├── Dockerfile.ubuntu.pip
│   ├── Dockerfile.debian.idp
│   └── Dockerfile.ubuntu.idp
├── docker-compose.yaml
├── horovod
│   ├── Dockerfile
│   ├── Dockerfile.mpich
│   └── Dockerfile.openmpi
├── inc
│   ├── Dockerfile
|   ├── Dockerfile.onnx
└── jupyter
    └── Dockerfile
```

[_docker-compose.yaml_](docker-compose.yaml)
```
version: '3'
services:
  tf-base:
    image: ${FINAL_IMAGE_NAME:-tf-base}-${BASE_IMAGE_NAME}-${PACKAGE_OPTION}:${TF_PACKAGE_VERSION:-2.9.1}
    build:
      context: ./base
      args:
        http_proxy: ${http_proxy}
        https_proxy: ${https_proxy}
        no_proxy: ${no_proxy}
        BASE_IMAGE_NAME: ${BASE_IMAGE_NAME:-ubuntu}
        BASE_IMAGE_TAG: ${BASE_IMAGE_TAG:-20.04}
        MINICONDA_VERSION: ${MINICONDA_VERSION}
        PACKAGE_OPTION: ${PACKAGE_OPTION}
        PYTHON_VERSION: ${PYTHON_VERSION}
        TF_PACKAGE_VERSION: ${TF_PACKAGE_VERSION:-2.9.1}
        TF_PACKAGE: ${TF_PACKAGE:-intel-tensorflow}
      dockerfile: Dockerfile.${BASE_IMAGE_NAME:-ubuntu}.${PACKAGE_OPTION}
    healthcheck: 
      test: curl --fail -I http://localhost:8080/status || exit 1
      interval: 10s
      timeout: 5s
      retries: 5
    command: >
      sh -c "python -c 'import tensorflow as tf; print(\"TensorFlow Version:\", tf.__version__)'"
...
```

### Build and Test with Make

```
$ make jupyter
WARN[0000] The "HOROVOD_VERSION" variable is not set. Defaulting to a blank string. 
WARN[0000] The "HOROVOD_VERSION" variable is not set. Defaulting to a blank string. 
[+] Building 0.8s (11/11) FINISHED                                                              
 => [internal] load build definition from Dockerfile.ubuntu.pip                            0.0s
 => => transferring dockerfile: 43B                                                        0.0s
 => [internal] load .dockerignore                                                          0.0s
 => => transferring context: 2B                                                            0.0s
 => [internal] load metadata for docker.io/library/ubuntu:20.04                            0.7s
 => [auth] library/ubuntu:pull token for registry-1.docker.io                              0.0s
 => [1/6] FROM docker.io/library/ubuntu:20.04@sha256:9c2004872a3a9fcec8cc757ad65c042de1da  0.0s
 => CACHED [2/6] RUN apt-get update && apt-get install -y --no-install-recommends --fix-m  0.0s
 => CACHED [3/6] RUN curl -fSsL https://bootstrap.pypa.io/get-pip.py | python3.8           0.0s
 => CACHED [4/6] RUN ln -sf $(which python3.8) /usr/local/bin/python &&     ln -sf $(whic  0.0s
 => CACHED [5/6] RUN python -m pip --no-cache-dir install --upgrade     pip     setuptool  0.0s
 => CACHED [6/6] RUN python -m pip install --no-cache-dir intel-tensorflow==2.10.0         0.0s
 => exporting to image                                                                     0.0s
 => => exporting layers                                                                    0.0s
 => => writing image sha256:d0ea79994e86d8867286f898bfdf412cdcbd6afcb89582dea1e54e4f82333  0.0s
 => => naming to docker.io/library/intel-tensorflow-ubuntu-pip:2.10.0                      0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
[+] Running 1/1
 ⠿ Container tensorflow-tf-base-1  Recreated                                               0.0s
Attaching to tensorflow-tf-base-1
tensorflow-tf-base-1  | 2022-10-07 18:52:55.441188: I tensorflow/core/platform/cpu_feature_guard.cc:193] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX2 AVX512F AVX512_VNNI FMA
tensorflow-tf-base-1  | To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
tensorflow-tf-base-1  | TensorFlow Version: 2.10.0
tensorflow-tf-base-1 exited with code 0
WARN[0000] The "HOROVOD_VERSION" variable is not set. Defaulting to a blank string. 
WARN[0000] The "HOROVOD_VERSION" variable is not set. Defaulting to a blank string. 
WARN[0000] The "MINICONDA_VERSION" variable is not set. Defaulting to a blank string. 
WARN[0000] The "PYTHON_VERSION" variable is not set. Defaulting to a blank string. 
[+] Building 0.1s (12/12) FINISHED                                                              
 => [internal] load build definition from Dockerfile                                       0.0s
 => => transferring dockerfile: 32B                                                        0.0s
 => [internal] load .dockerignore                                                          0.0s
 => => transferring context: 2B                                                            0.0s
 => [internal] load metadata for docker.io/library/intel-tensorflow-ubuntu-pip:2.10.0      0.0s
 => [1/8] FROM docker.io/library/intel-tensorflow-ubuntu-pip:2.10.0                        0.0s
 => CACHED [2/8] RUN python -m pip install --no-cache-dir jupyter matplotlib               0.0s
 => CACHED [3/8] RUN python -m pip install --no-cache-dir jupyter_http_over_ws ipykernel   0.0s
 => CACHED [4/8] RUN jupyter serverextension enable --py jupyter_http_over_ws              0.0s
 => CACHED [5/8] RUN mkdir -p /tf-base/ && chmod -R a+rwx /tf-base/                        0.0s
 => CACHED [6/8] RUN mkdir /.local && chmod a+rwx /.local                                  0.0s
 => CACHED [7/8] WORKDIR /tf-base                                                          0.0s
 => CACHED [8/8] RUN python -m ipykernel.kernelspec                                        0.0s
 => exporting to image                                                                     0.0s
 => => exporting layers                                                                    0.0s
 => => writing image sha256:0c07ccdbdbf99ad955b891acac45de54435edbc59c8253a773dc3ec69c55b  0.0s
 => => naming to docker.io/library/intel-tensorflow-ubuntu-pip:2.10.0-jupyter              0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
[+] Running 1/0
 ⠿ Container tensorflow-jupyter-1  Recreated                                               0.0s
Attaching to tensorflow-jupyter-1
tensorflow-jupyter-1  | 2022-10-07 18:52:58.025011: I tensorflow/core/platform/cpu_feature_guard.cc:193] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX2 AVX512F AVX512_VNNI FMA
tensorflow-jupyter-1  | To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
tensorflow-jupyter-1  | TensorFlow Version: 2.10.0
tensorflow-jupyter-1  | Selected Jupyter core packages...
tensorflow-jupyter-1  | IPython          : 8.5.0
tensorflow-jupyter-1  | ipykernel        : 6.16.0
tensorflow-jupyter-1  | ipywidgets       : 8.0.2
tensorflow-jupyter-1  | jupyter_client   : 7.3.5
tensorflow-jupyter-1  | jupyter_core     : 4.11.1
tensorflow-jupyter-1  | jupyter_server   : not installed
tensorflow-jupyter-1  | jupyterlab       : not installed
tensorflow-jupyter-1  | nbclient         : 0.7.0
tensorflow-jupyter-1  | nbconvert        : 7.2.1
tensorflow-jupyter-1  | nbformat         : 5.6.1
tensorflow-jupyter-1  | notebook         : 6.4.12
tensorflow-jupyter-1  | qtconsole        : 5.3.2
tensorflow-jupyter-1  | traitlets        : 5.4.0
tensorflow-jupyter-1 exited with code 0
```
