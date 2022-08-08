## Build and test TensorFlow Containers for Base, Jupyter, OpenMPI + Horovod and MPICH + Horovod

### Project structure:
```
├── Makefile
├── README.md
├── base
│   ├── Dockerfile.debian
│   ├── Dockerfile.ubuntu
│   └── config
│       ├── base.env
│       ├── debian.env
│       └── ubuntu.env
├── docker-compose.yaml
├── horovod
│   ├── Dockerfile
│   ├── Dockerfile.mpich
│   └── Dockerfile.openmpi
├── inc
│   ├── Dockerfile
└── jupyter
    └── Dockerfile
```

[_docker-compose.yaml_](docker-compose.yaml)
```
version: '3'
services:
  base:
    image: ${FINAL_IMAGE_NAME:-tf-base}:${TF_PACKAGE_VERSION:-2.9.1}
    build:
      context: ./base
      args:
        BASE_IMAGE_NAME: ${BASE_IMAGE_NAME:-ubuntu}
        BASE_IMAGE_TAG: ${BASE_IMAGE_TAG:-20.04}
        TF_PACKAGE: ${TF_PACKAGE:-intel-tensorflow}
        TF_PACKAGE_VERSION: ${TF_PACKAGE_VERSION:-2.9.1}
      dockerfile: Dockerfile.${BASE_IMAGE_NAME:-ubuntu}
    healthcheck:
      test: curl --fail -I http://localhost:8080/status || exit 1
      interval: 10s
      timeout: 5s
      retries: 5
    command: >
      sh -c "python -c 'import tensorflow as tf; print(\"TensorFlow Version:\", tf.__version__)'"

  jupyter:
    image: ${FINAL_IMAGE_NAME:-tf-base}:${TF_PACKAGE_VERSION:-2.9.1}-jupyter
    build:
      context: ./jupyter
      args:
        BASE_IMAGE_NAME: ${FINAL_IMAGE_NAME:-tf-base}
        BASE_IMAGE_TAG: ${TF_PACKAGE_VERSION:-2.9.1}
    healthcheck:
      test: curl --fail -I http://localhost:8080/status || exit 1
      interval: 10s
      timeout: 5s
      retries: 5
    ports:
      - ${PORT:-8888}:8888
    working_dir: /tf-base
    volumes:
      - ${PWD}:/tf-base
...
```

### Build with docker compose

```
$ docker compose build base jupyter

[+] Building 3.1s (22/22) FINISHED
 => [tf-base:2.9.1 internal] load build definition from Dockerfile.ubuntu                                                                                                                                            0.0s
 => => transferring dockerfile: 39B                                                                                                                                                                                  0.0s
 => [tf-base:2.9.1-jupyter internal] load build definition from Dockerfile                                                                                                                                           0.0s
 => => transferring dockerfile: 32B                                                                                                                                                                                  0.0s
 => [tf-base:2.9.1 internal] load .dockerignore                                                                                                                                                                      0.0s
 => => transferring context: 2B                                                                                                                                                                                      0.0s
 => [tf-base:2.9.1-jupyter internal] load .dockerignore                                                                                                                                                              0.0s
 => => transferring context: 2B                                                                                                                                                                                      0.0s
 => [tf-base:2.9.1 internal] load metadata for docker.io/library/ubuntu:20.04                                                                                                                                        2.8s
 => [tf-base:2.9.1-jupyter internal] load metadata for docker.io/library/tf-base:2.9.1                                                                                                                               0.0s
 => [tf-base:2.9.1-jupyter 1/8] FROM docker.io/library/tf-base:2.9.1                                                                                                                                                 0.0s
 => CACHED [tf-base:2.9.1-jupyter 2/8] RUN python -m pip install --no-cache-dir jupyter matplotlib                                                                                                                   0.0s
 => CACHED [tf-base:2.9.1-jupyter 3/8] RUN python -m pip install --no-cache-dir jupyter_http_over_ws ipykernel nbformat                                                                                              0.0s
 => CACHED [tf-base:2.9.1-jupyter 4/8] RUN jupyter serverextension enable --py jupyter_http_over_ws                                                                                                                  0.0s
 => CACHED [tf-base:2.9.1-jupyter 5/8] RUN mkdir -p /tf-base/ && chmod -R a+rwx /tf-base/                                                                                                                            0.0s
 => CACHED [tf-base:2.9.1-jupyter 6/8] RUN mkdir /.local && chmod a+rwx /.local                                                                                                                                      0.0s
 => CACHED [tf-base:2.9.1-jupyter 7/8] WORKDIR /tf-base                                                                                                                                                              0.0s
 => CACHED [tf-base:2.9.1-jupyter 8/8] RUN python -m ipykernel.kernelspec                                                                                                                                            0.0s
 => [tf-base:2.9.1] exporting to image                                                                                                                                                                               0.0s
 => => exporting layers                                                                                                                                                                                              0.0s
 => => writing image sha256:2128abe4122cf2a9561be52974c3beeb479e7c50ec090308f8b13836ad95ed9f                                                                                                                         0.0s
 => => naming to docker.io/library/tf-base:2.9.1-jupyter                                                                                                                                                             0.0s
 => => writing image sha256:12d95a4fe6f00f2f6a2fe5598e624cbc0bced8ae4ae59aa1c72bf7e287416c4b                                                                                                                         0.0s
 => => naming to docker.io/library/tf-base:2.9.1                                                                                                                                                                     0.0s
 => [auth] library/ubuntu:pull token for registry-1.docker.io                                                                                                                                                        0.0s
 => [tf-base:2.9.1 1/6] FROM docker.io/library/ubuntu:20.04@sha256:fd92c36d3cb9b1d027c4d2a72c6bf0125da82425fc2ca37c414d4f010180dc19                                                                                  0.0s
 => CACHED [tf-base:2.9.1 2/6] RUN apt-get update && apt-get install -y --no-install-recommends --fix-missing     ca-certificates     curl     python3     python3-distutils                                         0.0s
 => CACHED [tf-base:2.9.1 3/6] RUN curl -fSsL https://bootstrap.pypa.io/get-pip.py | python3                                                                                                                         0.0s
 => CACHED [tf-base:2.9.1 4/6] RUN ln -sf $(which python3) /usr/local/bin/python &&     ln -sf $(which python3) /usr/local/bin/python3 &&     ln -sf $(which python3) /usr/bin/python                                0.0s
 => CACHED [tf-base:2.9.1 5/6] RUN python -m pip --no-cache-dir install --upgrade     pip     setuptools                                                                                                             0.0s
 => CACHED [tf-base:2.9.1 6/6] RUN python -m pip install --no-cache-dir intel-tensorflow==2.9.1
```

### Deploy with docker compose

```
$ docker compose up -d base jupyter
[+] Running 3/3
 ⠿ Network tensorflow_default      Created                                                                                                                                                                           0.1s
 ⠿ Container tensorflow-jupyter-1  Started                                                                                                                                                                           0.9s
 ⠿ Container tensorflow-base-1     Started                                                                                                                                                                           0.8s
```

### Expected result

Listing containers must show one container running and the port mapping as below:
```
$ docker compose ps
NAME                   COMMAND                  SERVICE             STATUS               PORTS
tensorflow-base-1      "sh -c 'python -c 'i…"   base                exited (0)
tensorflow-jupyter-1   "bash -c 'source /et…"   jupyter             running (starting)   0.0.0.0:8888->8888/tcp
```

### Checking logs:
```
tensorflow-base-1  | TensorFlow Version: 2.9.1
tensorflow-jupyter-1  | [I 06:05:30.535 NotebookApp] Writing notebook server cookie secret to /root/.local/share/jupyter/runtime/notebook_cookie_secret
tensorflow-jupyter-1  | [I 06:05:30.841 NotebookApp] Serving notebooks from local directory:
tensorflow-jupyter-1  | [I 06:05:30.842 NotebookApp] Jupyter Notebook 6.4.12 is running at:
tensorflow-jupyter-1  | [I 06:05:30.842 NotebookApp] http://********:8888/?token=********
tensorflow-jupyter-1  | [I 06:05:30.842 NotebookApp]  or http://127.0.0.1:8888/?token=********
tensorflow-jupyter-1  | [I 06:05:30.842 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
tensorflow-jupyter-1  | [C 06:05:30.848 NotebookApp]
tensorflow-jupyter-1  |
tensorflow-jupyter-1  |     To access the notebook, open this file in a browser:
tensorflow-jupyter-1  |         file:///root/.local/share/jupyter/runtime/nbserver-1-open.html
tensorflow-jupyter-1  |     Or copy and paste one of these URLs:
tensorflow-jupyter-1  |         http://********:8888/?token=********
tensorflow-jupyter-1  |      or http://127.0.0.1:8888/?token=********
```

After the Jupyter container starts, navigate to `http://localhost:8888` in your web browser.

### Stop and remove the containers
```
$ docker compose down
[+] Running 3/3
 ⠿ Container tensorflow-jupyter-1  Removed                                                                                                                                                                           0.4s
 ⠿ Container tensorflow-base-1     Removed                                                                                                                                                                           0.0s
 ⠿ Network tensorflow_default      Removed                                                                                                                                                                           0.1s
```
