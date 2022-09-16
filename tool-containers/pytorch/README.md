## Build and test PyTorch + IPEX Containers for Base, OpenMPI + Horovod and MPICH + Horovod

### Project structure:
```
.
├── Makefile
├── README.md
├── base
│   ├── Dockerfile.ubuntu
│   └── config
│       └── ubuntu.env
├── docker-compose.yaml
└── horovod
    ├── Dockerfile
    ├── Dockerfile.mpich
    └── Dockerfile.openmpi

3 directories, 8 files
```

[_docker-compose.yaml_](docker-compose.yaml)
```
version: '3'
services:
  base:
    image: ${FINAL_IMAGE_NAME:-ipex-base}-${BASE_IMAGE_NAME}-${PACKAGE_OPTION}:${IPEX_PACKAGE_VERSION:-1.12.100}
    build:
      context: ./base
      args:
        BASE_IMAGE_NAME: ${BASE_IMAGE_NAME:-ubuntu}
        BASE_IMAGE_TAG: ${BASE_IMAGE_TAG:-20.04}
        IPEX_PACKAGE_VERSION: ${IPEX_PACKAGE_VERSION:-1.12.100}
        PACKAGE_OPTION: ${PACKAGE_OPTION}
      dockerfile: Dockerfile.${BASE_IMAGE_NAME:-ubuntu}.${PACKAGE_OPTION}
    healthcheck:
      test: curl --fail -I http://localhost:8080/status || exit 1
      interval: 10s
      timeout: 5s
      retries: 5
    command: >
      sh -c "python -c 'import torch; import intel_extension_for_pytorch as ipex; print(\"torch:\", torch.__version__, \" ipex:\",ipex.__version__)'"

  openmpi:
    image: ${FINAL_IMAGE_NAME:-ipex-base}-${BASE_OS_NAME}-${PACKAGE_OPTION}:${IPEX_PACKAGE_VERSION:-1.12.100}-openmpi
    build:
      context: ./horovod
      dockerfile: Dockerfile.openmpi
      args:
        BASE_IMAGE_NAME: ${FINAL_IMAGE_NAME:-ipex-base}
        BASE_IMAGE_TAG: ${IPEX_PACKAGE_VERSION:-1.12.100}
        BASE_OS_NAME: ${BASE_OS_NAME:-debian}
        PACKAGE_OPTION: ${PACKAGE_OPTION}
    healthcheck:
      test: curl --fail -I http://localhost:8080/status || exit 1
      interval: 10s
      timeout: 5s
      retries: 5
    command: >
      sh -c "python -c 'import torch; import intel_extension_for_pytorch as ipex; print(\"torch:\", torch.__version__, \" ipex:\",ipex.__version__)' && 
             mpirun --version"
...
```

### Build with docker compose

```
$ docker compose build base openmpi

base openmpi
[+] Building 0.3s (13/13) FINISHED                                                                                                                                                                                                                                                         
 => [internal] load build definition from Dockerfile.ubuntu                                                                                                                                                                                                                           0.0s
 => => transferring dockerfile: 39B                                                                                                                                                                                                                                                   0.0s
 => [internal] load .dockerignore                                                                                                                                                                                                                                                     0.0s
 => => transferring context: 2B                                                                                                                                                                                                                                                       0.0s
 => resolve image config for docker.io/docker/dockerfile:1                                                                                                                                                                                                                            0.0s
 => CACHED docker-image://docker.io/docker/dockerfile:1                                                                                                                                                                                                                               0.0s
 => [internal] load build definition from Dockerfile.ubuntu                                                                                                                                                                                                                           0.0s
 => [internal] load .dockerignore                                                                                                                                                                                                                                                     0.0s
 => [internal] load metadata for docker.io/library/ubuntu:20.04                                                                                                                                                                                                                       0.0s
 => [1/5] FROM docker.io/library/ubuntu:20.04                                                                                                                                                                                                                                         0.0s
 => CACHED [2/5] RUN apt-get update -y &&     apt-get upgrade -y &&     apt-get install -y --no-install-recommends --fix-missing     python3     python3-pip                                                                                                                          0.0s
 => CACHED [3/5] RUN python3 -m pip --no-cache-dir install --upgrade     pip     setuptools     psutil                                                                                                                                                                                0.0s
 => CACHED [4/5] RUN ln -s $(which python3) /usr/local/bin/python                                                                                                                                                                                                                     0.0s
 => CACHED [5/5] RUN     python -m pip install --no-cache-dir     torch==1.12.0+cpu torchvision==0.13.0+cpu torchaudio==0.12.0 -f https://download.pytorch.org/whl/cpu/torch_stable.html &&     python -m pip install --no-cache-dir     intel_extension_for_pytorch==1.12.100 -f ht  0.0s
 => exporting to image                                                                                                                                                                                                                                                                0.0s
 => => exporting layers                                                                                                                                                                                                                                                               0.0s
 => => writing image sha256:c121b7ad17d882f67cfc569d28bba08fbabf83fd626247f36f0f314ffd396528                                                                                                                                                                                          0.0s
 => => naming to docker.io/library/ipex-base:1.12.100                                                                                                                                                                                                                                 0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
[+] Building 0.1s (10/10) FINISHED                                                                                                                                                                                                                                                         
 => [internal] load build definition from Dockerfile.openmpi                                                                                                                                                                                                                          0.0s
 => => transferring dockerfile: 2.13kB                                                                                                                                                                                                                                                0.0s
 => [internal] load .dockerignore                                                                                                                                                                                                                                                     0.0s
 => => transferring context: 2B                                                                                                                                                                                                                                                       0.0s
 => [internal] load metadata for docker.io/library/ipex-base:1.12.100                                                                                                                                                                                                                 0.0s
 => [1/6] FROM docker.io/library/ipex-base:1.12.100                                                                                                                                                                                                                                   0.0s
 => CACHED [2/6] RUN apt-get update && apt-get install -y --no-install-recommends --fix-missing     libopenmpi-dev     openmpi-bin     openmpi-common     openssh-client     openssh-server &&     apt-get clean &&     rm -rf /var/lib/apt/lists/*                                   0.0s
 => CACHED [3/6] RUN mv /usr/bin/mpirun /usr/bin/mpirun.real &&     echo '#!/bin/bash' > /usr/bin/mpirun &&     echo 'mpirun.real --allow-run-as-root "$@"' >> /usr/bin/mpirun &&     chmod a+x /usr/bin/mpirun                                                                       0.0s
 => CACHED [4/6] RUN echo "btl_tcp_if_exclude = lo,docker0" >> /etc/openmpi/openmpi-mca-params.conf                                                                                                                                                                                   0.0s
 => CACHED [5/6] RUN mkdir -p /var/run/sshd                                                                                                                                                                                                                                           0.0s
 => CACHED [6/6] RUN cat /etc/ssh/ssh_config | grep -v StrictHostKeyChecking > /etc/ssh/ssh_config.new &&     echo "    StrictHostKeyChecking no" >> /etc/ssh/ssh_config.new &&     mv /etc/ssh/ssh_config.new /etc/ssh/ssh_config                                                    0.0s
 => exporting to image                                                                                                                                                                                                                                                                0.0s
 => => exporting layers                                                                                                                                                                                                                                                               0.0s
 => => writing image sha256:3036426804aff853d01bf16ab1c37719fbfe8974b0623f55f8a0838fbc330449                                                                                                                                                                                          0.0s
 => => naming to docker.io/library/ipex-base:1.12.100-openmpi                                                                                       
```

### Deploy with docker compose

```
$ docker compose up -d base openmpi
[+] Running 3/3
 ⠿ Network pytorch_default      Created                                                                                                                                                                                                                                               0.4s
 ⠿ Container pytorch-openmpi-1  Started                                                                                                                                                                                                                                               0.8s
 ⠿ Container pytorch-base-1     Started 
```

### Expected result

Listing containers must show one container running and the port mapping as below:
```
$ docker compose ps
$ docker compose ps
NAME                COMMAND                  SERVICE             STATUS              PORTS
pytorch-base-1      "sh -c 'python -c 'i…"   base                exited (0)          
pytorch-openmpi-1   "sh -c 'python -c 'i…"   openmpi             exited (0)          
```

### Checking logs:
```
pytorch-openmpi-1  | torch: 1.12.0+cpu  ipex: 1.12.100
pytorch-openmpi-1  | mpirun.real (OpenRTE) 4.0.3
pytorch-openmpi-1  | 
pytorch-openmpi-1  | Report bugs to http://www.open-mpi.org/community/help/
pytorch-base-1     | torch: 1.12.0+cpu  ipex: 1.12.100
```

### Stop and remove the containers
```
$ docker compose down
[+] Running 3/3
 ⠿ Container pytorch-base-1     Removed                                                                                                                                                                                                                                               0.0s
 ⠿ Container pytorch-openmpi-1  Removed                                                                                                                                                                                                                                               0.0s
 ⠿ Network pytorch_default      Removed 
```
