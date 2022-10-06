## Build and test TensorFlow Containers for Base, Jupyter, OpenMPI + Horovod and MPICH + Horovod

### Project structure:
```
├── Makefile
├── README.md
├── base
│   ├── Dockerfile.debian.pip
│   ├── Dockerfile.ubuntu.pip
│   ├── Dockerfile.debian.idp
│   ├── Dockerfile.ubuntu.idp
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
    image: ${FINAL_IMAGE_NAME:-tf-base}-${BASE_IMAGE_NAME}-${PACKAGE_OPTION}:${TF_PACKAGE_VERSION:-2.9.1}
    build:
      context: ./base
      args:
        BASE_IMAGE_NAME: ${BASE_IMAGE_NAME:-ubuntu}
        BASE_IMAGE_TAG: ${BASE_IMAGE_TAG:-20.04}
        TF_PACKAGE: ${TF_PACKAGE:-intel-tensorflow}
        TF_PACKAGE_VERSION: ${TF_PACKAGE_VERSION:-2.9.1}
        PACKAGE_OPTION: ${PACKAGE_OPTION}
      dockerfile: Dockerfile.${BASE_IMAGE_NAME:-ubuntu}
    healthcheck:
      test: curl --fail -I http://localhost:8080/status || exit 1
      interval: 10s
      timeout: 5s
      retries: 5
    command: >
      sh -c "python -c 'import tensorflow as tf; print(\"TensorFlow Version:\", tf.__version__)'"

  jupyter:
    image: ${FINAL_IMAGE_NAME:-tf-base}-${BASE_IMAGE_NAME}-${PACKAGE_OPTION}:${TF_PACKAGE_VERSION:-2.9.1}-jupyter
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

#1 [tf-base-ubuntu-idp:2.9.1-jupyter internal] load build definition from Dockerfile
#1 transferring dockerfile: 32B done
#1 DONE 0.0s

#2 [tf-base-ubuntu-idp:2.9.1 internal] load build definition from Dockerfile.ubuntu.idp
#2 transferring dockerfile: 43B done
#2 DONE 0.0s

#3 [tf-base-ubuntu-idp:2.9.1 internal] load .dockerignore
#3 transferring context: 2B done
#3 DONE 0.0s

#4 [tf-base-ubuntu-idp:2.9.1-jupyter internal] load .dockerignore
#4 transferring context: 2B done
#4 DONE 0.0s

#5 [tf-base-ubuntu-idp:2.9.1-jupyter internal] load metadata for docker.io/library/tf-base-ubuntu-idp:2.9.1
#5 DONE 0.0s

#6 [tf-base-ubuntu-idp:2.9.1 internal] load metadata for docker.io/library/ubuntu:20.04
#6 DONE 0.0s

#7 [tf-base-ubuntu-idp:2.9.1 1/6] FROM docker.io/library/ubuntu:20.04
#7 CACHED

#8 [tf-base-ubuntu-idp:2.9.1-jupyter 1/8] FROM docker.io/library/tf-base-ubuntu-idp:2.9.1
#8 CACHED

...
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
