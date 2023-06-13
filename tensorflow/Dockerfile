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

ARG BASE_IMAGE_NAME=ubuntu
ARG BASE_IMAGE_TAG=22.04
ARG PACKAGE_OPTION=pip
ARG MPI=openmpi

FROM ${BASE_IMAGE_NAME}:${BASE_IMAGE_TAG} AS base

# Intel Optimizations specific Envs
ENV KMP_AFFINITY='granularity=fine,verbose,compact,1,0' \
    KMP_BLOCKTIME=1 \
    KMP_SETTINGS=1

# See http://bugs.python.org/issue19846
ENV LANG C.UTF-8
ARG PYTHON_VERSION

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt-get update && apt-get install -y --no-install-recommends --fix-missing \
    ca-certificates \
    curl \
    wget

RUN echo "cat /fig.txt" >> ~/.bashrc

ARG TF_PACKAGE
ARG TF_PACKAGE_VERSION

# Add Intel TF Licensing
RUN	mkdir /licensing && \
    wget -O - https://github.com/Intel-tensorflow/tensorflow/archive/v${TF_PACKAGE_VERSION}.tar.gz | \
	tar -xz -C /licensing --strip=2 "tensorflow-${TF_PACKAGE_VERSION}/third_party_programs_license/" && \
    curl https://raw.githubusercontent.com/Intel-tensorflow/tensorflow/v${TF_PACKAGE_VERSION}/LICENSE -o /licensing/TF_LICENSE

FROM base AS tf-base-pip

RUN apt-get install -y --no-install-recommends --fix-missing \
    python${PYTHON_VERSION} \
    python3-pip \
    python${PYTHON_VERSION}-distutils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Some TF tools expect a "python" binary
RUN ln -sf $(which python${PYTHON_VERSION}) /usr/local/bin/python && \
    ln -sf $(which python${PYTHON_VERSION}) /usr/local/bin/python3 && \
    ln -sf $(which python${PYTHON_VERSION}) /usr/bin/python

RUN python -m pip --no-cache-dir install --upgrade \
    pip \
    setuptools

RUN python -m pip install --no-cache-dir ${TF_PACKAGE}${TF_PACKAGE_VERSION:+==${TF_PACKAGE_VERSION}}

FROM base AS tf-base-idp

ARG MINICONDA_VERSION

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-${MINICONDA_VERSION}.sh -O miniconda.sh && \        
    chmod +x miniconda.sh && \
    ./miniconda.sh -b -p ~/conda && \
    rm ./miniconda.sh && \
    ln -s ~/conda ~/miniconda3 && \
    export PATH=~/conda/bin/:${PATH} && \
    conda update -y conda && \
    conda config --add channels intel && \
    conda create -yn idp intelpython3_core python=${PYTHON_VERSION} && \
    conda init --all && \
    conda clean -y --all

# Avoid horovod and mpi from failing with incorrect gcc libraries
RUN rm -rf /root/conda/envs/idp/lib/libstdc++.so.6 && ln -s /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /root/conda/envs/idp/lib/libstdc++.so.6
RUN rm -rf /root/conda/envs/idp/lib/libtinfo.so.6 && ln -s /usr/lib/x86_64-linux-gnu/libtinfo.so.6 /root/conda/envs/idp/lib/libtinfo.so.6

ENV PATH /root/conda/condabin:~/conda/bin/:${PATH}
ENV LD_LIBRARY_PATH /lib64/:/usr/lib64/:/usr/local/lib64:/root/conda/envs/idp/lib:${LD_LIBRARY_PATH}

ENV TF_ENABLE_ONEDNN_OPTS=1
ARG TF_PACKAGE
ARG TF_PACKAGE_VERSION

RUN conda run -n idp python -m pip install --no-cache-dir ${TF_PACKAGE}${TF_PACKAGE_VERSION:+==${TF_PACKAGE_VERSION}}

RUN echo "conda activate idp" >> ~/.bashrc

RUN ln -sf /root/conda/envs/idp/bin/python /usr/local/bin/python && \
    ln -sf /root/conda/envs/idp/bin/python /usr/local/bin/python3 && \
    ln -sf /root/conda/envs/idp/bin/python /usr/bin/python

FROM tf-base-${PACKAGE_OPTION} AS jupyter

RUN python -m pip install --no-cache-dir jupyter matplotlib jupyter_http_over_ws ipykernel nbformat
RUN python -m jupyter serverextension enable --py jupyter_http_over_ws

RUN mkdir -p /tf-base/ && chmod -R a+rwx /tf-base/
RUN mkdir /.local && chmod a+rwx /.local
WORKDIR /tf-base
EXPOSE 8888

RUN python -m ipykernel.kernelspec

CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter notebook --notebook-dir=${WORKDIR} --ip 0.0.0.0 --no-browser --allow-root"]

FROM tf-base-${PACKAGE_OPTION} AS openmpi

# install libnuma, openssh, wget
RUN apt-get update -y && apt-get install -y --no-install-recommends --fix-missing \
    libopenmpi-dev \
    openmpi-bin \
    openmpi-common \
    openssh-client \
    openssh-server

# Create a wrapper for OpenMPI to allow running AS root by default
RUN mv /usr/bin/mpirun /usr/bin/mpirun.real && \
    echo '#!/bin/bash' > /usr/bin/mpirun && \
    echo 'mpirun.real --allow-run-as-root "$@"' >> /usr/bin/mpirun && \
    chmod a+x /usr/bin/mpirun

# Configure OpenMPI to run good defaults:
RUN echo "btl_tcp_if_exclude = lo,docker0" >> /etc/openmpi/openmpi-mca-params.conf

# Install OpenSSH for MPI to communicate between containers
RUN mkdir -p /var/run/sshd

# Allow OpenSSH to talk to containers without asking for confirmation
RUN cat /etc/ssh/ssh_config | grep -v StrictHostKeyChecking > /etc/ssh/ssh_config.new && \
    echo "    StrictHostKeyChecking no" >> /etc/ssh/ssh_config.new && \
    mv /etc/ssh/ssh_config.new /etc/ssh/ssh_config

FROM tf-base-${PACKAGE_OPTION} AS mpich

# install libnuma, openssh, wget
RUN apt-get update -y && apt-get install -y --no-install-recommends --fix-missing \
    mpich \
    libmpich-dev \
    openssh-client \
    openssh-server

# Create a wrapper for MPICH to allow running AS root by default
RUN mv /usr/bin/mpirun /usr/bin/mpirun.real && \
    echo '#!/bin/bash' > /usr/bin/mpirun && \
    echo 'mpirun.real "$@"' >> /usr/bin/mpirun && \
    chmod a+x /usr/bin/mpirun

# Install OpenSSH for MPI to communicate between containers
RUN mkdir -p /var/run/sshd

# Allow OpenSSH to talk to containers without asking for confirmation
RUN cat /etc/ssh/ssh_config | grep -v StrictHostKeyChecking > /etc/ssh/ssh_config.new && \
    echo "    StrictHostKeyChecking no" >> /etc/ssh/ssh_config.new && \
    mv /etc/ssh/ssh_config.new /etc/ssh/ssh_config

FROM ${MPI} AS horovod

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
    python3-dev

RUN python -m pip install --no-cache-dir horovod${HOROVOD_VERSION+==${HOROVOD_VERSION}}

FROM horovod AS inc

RUN apt-get install -y --no-install-recommends --fix-missing \
    libgl1-mesa-glx \
    libglib2.0-0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ARG INC_VER

ENV SIGOPT_PROJECT=.

RUN python -m pip install --no-cache-dir neural-compressor${INC_VER:+==${INC_VER}} \
    numpy==1.23.1 \
    tf2onnx

RUN curl https://raw.githubusercontent.com/intel/neural-compressor/master/docker/third-party-programs-tensorflow.txt -o /licensing/third-party-programs-tensorflow.txt && \
    curl https://raw.githubusercontent.com/intel/neural-compressor/v${INC_VER}/LICENSE -o /licensing/INC_LICENSE
