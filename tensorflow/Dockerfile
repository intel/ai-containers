# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
#
#
# This file was assembled from multiple pieces, whose use is documented
# throughout. Please refer to the TensorFlow dockerfiles documentation
# for more information.

ARG PACKAGE_OPTION=pip
ARG MPI=openmpi

ARG COMPOSE_PROJECT_NAME
FROM ${COMPOSE_PROJECT_NAME}-python AS tf-base-pip

# Intel Optimizations specific Envs
ENV KMP_AFFINITY='granularity=fine,verbose,compact,1,0' \
    KMP_BLOCKTIME=1 \
    KMP_SETTINGS=1

ARG TF_PACKAGE
ARG TF_PACKAGE_VERSION

RUN python -m pip install --no-cache-dir ${TF_PACKAGE}${TF_PACKAGE_VERSION:+==${TF_PACKAGE_VERSION}} \
    tensorflow_hub \
    Pillow \
    cryptography==41.0.3

# Add Intel TF Licensing
RUN	mkdir /licensing && \
    wget -O - https://github.com/Intel-tensorflow/tensorflow/archive/v${TF_PACKAGE_VERSION}.tar.gz | \
	tar -xz -C /licensing --strip=2 "tensorflow-${TF_PACKAGE_VERSION}/third_party_programs_license/" && \
    curl --insecure https://raw.githubusercontent.com/Intel-tensorflow/tensorflow/v${TF_PACKAGE_VERSION}/LICENSE -o /licensing/TF_LICENSE

FROM ${COMPOSE_PROJECT_NAME}-python AS tf-base-idp

# Intel Optimizations specific Envs
ENV KMP_AFFINITY='granularity=fine,verbose,compact,1,0' \
    KMP_BLOCKTIME=1 \
    KMP_SETTINGS=1

ENV PATH /usr/bin:/root/conda/envs/idp/bin:/root/conda/condabin:~/conda/bin/:${PATH}
ENV LD_LIBRARY_PATH /root/conda/envs/idp/lib:/lib64/:/usr/lib64/:/usr/local/lib64:${LD_LIBRARY_PATH}

ENV TF_ENABLE_ONEDNN_OPTS=1
ARG TF_PACKAGE
ARG TF_PACKAGE_VERSION

RUN python -m pip install --no-cache-dir ${TF_PACKAGE}${TF_PACKAGE_VERSION:+==${TF_PACKAGE_VERSION}} \
    tensorflow_hub \
    Pillow \
    certifi==2023.7.22 \
    cryptography==41.0.3 \
    scipy==1.11.1

# Add Intel TF Licensing
RUN	mkdir /licensing && \
    wget -O - https://github.com/Intel-tensorflow/tensorflow/archive/v${TF_PACKAGE_VERSION}.tar.gz | \
	tar -xz -C /licensing --strip=2 "tensorflow-${TF_PACKAGE_VERSION}/third_party_programs_license/" && \
    curl --insecure https://raw.githubusercontent.com/Intel-tensorflow/tensorflow/v${TF_PACKAGE_VERSION}/LICENSE -o /licensing/TF_LICENSE

FROM tf-base-${PACKAGE_OPTION} AS jupyter

RUN python -m pip install --no-cache-dir jupyterlab jupyterhub notebook jupyter-server-proxy

RUN mkdir -p /jupyter/ && chmod -R a+rwx /jupyter/
RUN mkdir /.local && chmod a+rwx /.local
WORKDIR /jupyter

ARG PORT=8888
EXPOSE $PORT

CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter notebook --notebook-dir=/jupyter --port $PORT --ip 0.0.0.0 --no-browser --allow-root"]

FROM tf-base-${PACKAGE_OPTION} AS mlflow

RUN python -m pip install --no-cache-dir mlflow

ARG PORT=5000
EXPOSE $PORT

CMD ["mlflow", "server", "-h", "0.0.0.0", "-p", $PORT]

FROM tf-base-${PACKAGE_OPTION} AS openmpi

RUN apt-get update -y && apt-get install -y --no-install-recommends --fix-missing \
    libopenmpi-dev \
    openmpi-bin \
    openmpi-common

FROM tf-base-${PACKAGE_OPTION} AS mpich

RUN apt-get update -y && apt-get install -y --no-install-recommends --fix-missing \
    mpich \
    libmpich-dev

RUN python -m pip install --no-cache-dir impi-rt

FROM ${MPI} AS horovod

RUN apt-get install -y --only-upgrade --no-install-recommends --fix-missing \
    openssh-client \
    openssh-server

ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

ENV OMPI_MCA_tl_tcp_if_exclude="lo,docker0"

# Install OpenSSH for MPI to communicate between containers
RUN mkdir -p /var/run/sshd

# Install Horovod
ARG HOROVOD_VERSION
ARG HOROVOD_WITH_TENSORFLOW=1
ARG HOROVOD_WITHOUT_MXNET=1
ARG HOROVOD_WITHOUT_PYTORCH=1
ARG HOROVOD_WITHOUT_GLOO=1
ARG HOROVOD_WITH_MPI=1

RUN apt-get install -y --no-install-recommends --fix-missing \
    build-essential \
    cmake \
    g++ \
    gcc \
    git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir horovod${HOROVOD_VERSION+==${HOROVOD_VERSION}}

ARG INC_VER

ENV SIGOPT_PROJECT=.

RUN curl --insecure https://raw.githubusercontent.com/intel/neural-compressor/master/docker/third-party-programs-tensorflow.txt -o /licensing/third-party-programs-tensorflow.txt && \
    curl --insecure https://raw.githubusercontent.com/intel/neural-compressor/master/LICENSE -o /licensing/LICENSE

FROM horovod AS multinode-pip

RUN python -m pip install --no-cache-dir neural-compressor${INC_VER:+==${INC_VER}} \
    tf2onnx

FROM horovod AS multinode-idp

RUN python -m pip install --no-cache-dir neural-compressor${INC_VER:+==${INC_VER}} \
    cython \
    tf2onnx
