## Build and test PyTorch + IPEX Containers for Base, OpenMPI + Horovod and MPICH + Horovod

### Project structure:
```
.
├── Makefile
├── README.md
├── base
│   ├── Dockerfile.debian.idp
│   ├── Dockerfile.debian.pip
│   ├── Dockerfile.ubuntu.idp
│   ├── Dockerfile.ubuntu.pip
│   └── config
│       └── ubuntu.env
├── docker-compose.yaml
├── horovod
│   ├── Dockerfile
│   ├── Dockerfile.mpich
│   └── Dockerfile.openmpi
└── inc
    └── Dockerfile

4 directories, 12 files
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
[+] Building 1.0s (23/23) FINISHED                                                                                                                                                                                       
 => [ipex-base-debian-idp:1.12.100-openmpi internal] load build definition from Dockerfile.openmpi                                                                                                                  0.0s
 => => transferring dockerfile: 40B                                                                                                                                                                                 0.0s
 => [ipex-base-debian-idp:1.12.100 internal] load build definition from Dockerfile.debian.idp                                                                                                                       0.0s
 => => transferring dockerfile: 43B                                                                                                                                                                                 0.0s
 => [ipex-base-debian-idp:1.12.100-openmpi internal] load .dockerignore                                                                                                                                             0.0s
 => => transferring context: 2B                                                                                                                                                                                     0.0s
 => [ipex-base-debian-idp:1.12.100 internal] load .dockerignore                                                                                                                                                     0.0s
 => => transferring context: 2B                                                                                                                                                                                     0.0s
 => [ipex-base-debian-idp:1.12.100-openmpi internal] load metadata for docker.io/library/ipex-base-debian-idp:1.12.100                                                                                              0.0s
 => [ipex-base-debian-idp:1.12.100-openmpi 1/6] FROM docker.io/library/ipex-base-debian-idp:1.12.100                                                                                                                0.0s
 => CACHED [ipex-base-debian-idp:1.12.100-openmpi 2/6] RUN apt-get update && apt-get install -y --no-install-recommends --fix-missing     libopenmpi-dev     openmpi-bin     openmpi-common     openssh-client      0.0s
 => CACHED [ipex-base-debian-idp:1.12.100-openmpi 3/6] RUN mv /usr/bin/mpirun /usr/bin/mpirun.real &&     echo '#!/bin/bash' > /usr/bin/mpirun &&     echo 'mpirun.real --allow-run-as-root "$@"' >> /usr/bin/mpir  0.0s
 => CACHED [ipex-base-debian-idp:1.12.100-openmpi 4/6] RUN echo "btl_tcp_if_exclude = lo,docker0" >> /etc/openmpi/openmpi-mca-params.conf                                                                           0.0s
 => CACHED [ipex-base-debian-idp:1.12.100-openmpi 5/6] RUN mkdir -p /var/run/sshd                                                                                                                                   0.0s
 => CACHED [ipex-base-debian-idp:1.12.100-openmpi 6/6] RUN cat /etc/ssh/ssh_config | grep -v StrictHostKeyChecking > /etc/ssh/ssh_config.new &&     echo "    StrictHostKeyChecking no" >> /etc/ssh/ssh_config.new  0.0s
 => [ipex-base-debian-idp:1.12.100] exporting to image                                                                                                                                                              0.0s
 => => exporting layers                                                                                                                                                                                             0.0s
 => => writing image sha256:92243680da9c23485af706718eecb8e119a15d1dc2ca4f33fba2124efc0b63ca                                                                                                                        0.0s
 => => naming to docker.io/library/ipex-base-debian-idp:1.12.100-openmpi                                                                                                                                            0.0s
 => => writing image sha256:09f361a0ddd1b4885e9187b3429d9e3ad1a2b59afef0f2adeb831c6377bf7ae1                                                                                                                        0.0s
 => => naming to docker.io/library/ipex-base-debian-idp:1.12.100                                                                                                                                                    0.0s
 => [ipex-base-debian-idp:1.12.100] resolve image config for docker.io/docker/dockerfile:1                                                                                                                          0.4s
 => CACHED [ipex-base-debian-idp:1.12.100] docker-image://docker.io/docker/dockerfile:1@sha256:9ba7531bd80fb0a858632727cf7a112fbfd19b17e94c4e84ced81e24ef1a0dbc                                                     0.0s
 => [ipex-base-debian-idp:1.12.100 internal] load .dockerignore                                                                                                                                                     0.0s
 => [ipex-base-debian-idp:1.12.100 internal] load build definition from Dockerfile.debian.idp                                                                                                                       0.0s
 => [ipex-base-debian-idp:1.12.100 internal] load metadata for docker.io/library/debian:11                                                                                                                          0.4s
 => [ipex-base-debian-idp:1.12.100 1/6] FROM docker.io/library/debian:11@sha256:3e82b1af33607aebaeb3641b75d6e80fd28d36e17993ef13708e9493e30e8ff9                                                                    0.0s
 => CACHED [ipex-base-debian-idp:1.12.100 2/6] RUN apt-get update -y &&     apt-get install -y     wget                                                                                                             0.0s
 => CACHED [ipex-base-debian-idp:1.12.100 3/6] RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py38_4.12.0-Linux-x86_64.sh -O miniconda.sh &&     chmod +x miniconda.sh &&     ./miniconda.sh -b -  0.0s
 => CACHED [ipex-base-debian-idp:1.12.100 4/6] RUN source activate idp &&     pip install     setuptools     psutil     torch==1.12.0+cpu torchvision==0.13.0+cpu torchaudio==0.12.0 -f https://download.pytorch.o  0.0s
 => CACHED [ipex-base-debian-idp:1.12.100 5/6] RUN echo "source ~/conda/etc/profile.d/conda.sh" >> /root/.bash_profile &&     echo "conda activate idp" >> /root/.bash_profile                                      0.0s
 => CACHED [ipex-base-debian-idp:1.12.100 6/6] RUN apt-get clean                                                                                                                                                    0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them                                                                                   
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
