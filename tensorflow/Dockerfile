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

ARG REGISTRY
ARG REPO
ARG GITHUB_RUN_NUMBER
ARG BASE_IMAGE_NAME
ARG BASE_IMAGE_TAG
ARG PACKAGE_OPTION=pip
ARG PYTHON_VERSION
ARG PYTHON_BASE=${REGISTRY}/${REPO}:b-${GITHUB_RUN_NUMBER}-${BASE_IMAGE_NAME}-${BASE_IMAGE_TAG}-${PACKAGE_OPTION}-py${PYTHON_VERSION}-base
FROM ${PYTHON_BASE} AS tf-base-pip

# Intel Optimizations specific Envs
ENV KMP_AFFINITY='granularity=fine,verbose,compact,1,0' \
    KMP_BLOCKTIME=1 \
    KMP_SETTINGS=1

ARG TF_VERSION

WORKDIR /
COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt

ADD https://raw.githubusercontent.com/intel/intel-extension-for-tensorflow/master/third-party-programs/dockerlayer/THIRD-PARTY-PROGRAMS.txt /licenses/
ADD https://raw.githubusercontent.com/intel/intel-extension-for-tensorflow/master/third-party-programs/dockerlayer/third-party-program-of-intel-extension-for-tensorflow.txt /licenses/

FROM ${PYTHON_BASE} AS tf-base-idp

# Intel Optimizations specific Envs
ENV KMP_AFFINITY='granularity=fine,verbose,compact,1,0' \
    KMP_BLOCKTIME=1 \
    KMP_SETTINGS=1

ENV PATH /usr/bin:/root/conda/envs/idp/bin:/root/conda/condabin:~/conda/bin/:${PATH}

ENV TF_ENABLE_ONEDNN_OPTS=1
ARG TF_VERSION

WORKDIR /
COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt

ADD https://raw.githubusercontent.com/intel/intel-extension-for-tensorflow/master/third-party-programs/dockerlayer/THIRD-PARTY-PROGRAMS.txt /licenses/
ADD https://raw.githubusercontent.com/intel/intel-extension-for-tensorflow/master/third-party-programs/dockerlayer/third-party-program-of-intel-extension-for-tensorflow.txt /licenses/

FROM tf-base-${PACKAGE_OPTION} AS jupyter

WORKDIR /jupyter
COPY jupyter-requirements.txt .

RUN python -m pip install --no-cache-dir -r jupyter-requirements.txt

RUN mkdir -p /jupyter/ && chmod -R a+rwx /jupyter/
RUN mkdir /.local && chmod a+rwx /.local

EXPOSE 8888

CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter notebook --notebook-dir=/jupyter --port 8888 --ip 0.0.0.0 --no-browser --allow-root --ServerApp.token= --ServerApp.password= --ServerApp.allow_origin=* --ServerApp.base_url=$NB_PREFIX"]

FROM tf-base-${PACKAGE_OPTION} AS openmpi

RUN apt-get update -y && apt-get install -y --no-install-recommends --fix-missing \
    libopenmpi-dev \
    openmpi-bin \
    openmpi-common

WORKDIR /
COPY ompi-requirements.txt .

RUN python -m pip install --no-cache-dir -r ompi-requirements.txt

FROM openmpi AS horovod

ENV LD_LIBRARY_PATH /lib64/:/usr/lib64/:/usr/local/lib64

RUN apt-get install -y --no-install-recommends --fix-missing \
    unzip \
    openssh-client \
    openssh-server && \
    rm  /etc/ssh/ssh_host_*_key \
        /etc/ssh/ssh_host_*_key.pub

ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

ENV OMPI_MCA_tl_tcp_if_exclude="lo,docker0"

# Install OpenSSH for MPI to communicate between containers
RUN mkdir -p /var/run/sshd && \
    echo 'LoginGraceTime 0' > /etc/ssh/sshd_config

# Install Horovod
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

WORKDIR /
COPY hvd-requirements.txt .

RUN python -m pip install --no-cache-dir -r hvd-requirements.txt

ENV SIGOPT_PROJECT=.

RUN wget --progress=dot:giga --no-check-certificate https://github.com/intel/neural-compressor/raw/master/docker/third-party-programs-tensorflow.txt -O /licenses/inc-third-party-programs-tensorflow.txt && \
    wget --progress=dot:giga --no-check-certificate https://raw.githubusercontent.com/intel/neural-compressor/master/LICENSE -O /licenses/INC_LICENSE

FROM horovod AS multinode-pip

WORKDIR /
COPY multinode-requirements.txt .

RUN python -m pip install --no-cache-dir -r multinode-requirements.txt

FROM horovod AS multinode-idp

WORKDIR /
COPY multinode-requirements.txt .

RUN python -m pip install --no-cache-dir -r multinode-requirements.txt

FROM ${PYTHON_BASE} AS itex-xpu-base-pip

RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
    apt-utils \
    build-essential \
    clinfo \
    git \
    gnupg2 \
    gpg-agent \
    rsync \
    unzip \
    wget && \
    apt-get clean && \
    rm -rf  /var/lib/apt/lists/*

ARG ICD_VER
ARG LEVEL_ZERO_GPU_VER
ARG LEVEL_ZERO_VER
ARG LEVEL_ZERO_DEV_VER
ARG DPCPP_VER
ARG MKL_VER
ARG CCL_VER

RUN no_proxy="" NO_PROXY="" wget --no-check-certificate -qO - https://repositories.intel.com/gpu/intel-graphics.key | \
    gpg --dearmor --output /usr/share/keyrings/intel-graphics.gpg
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/intel-graphics.gpg] https://repositories.intel.com/gpu/ubuntu jammy/lts/2350 unified" | \
    tee /etc/apt/sources.list.d/intel-gpu-jammy.list

RUN no_proxy="" NO_PROXY="" apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
    intel-opencl-icd=${ICD_VER} \
    intel-level-zero-gpu=${LEVEL_ZERO_GPU_VER} \
    level-zero=${LEVEL_ZERO_VER} \
    level-zero-dev=${LEVEL_ZERO_DEV_VER} && \
    apt-get clean && \
    rm -rf  /var/lib/apt/lists/*

RUN no_proxy="" NO_PROXY="" wget --progress=dot:giga -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB \
   | gpg --dearmor | tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null && \
   echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" \
   | tee /etc/apt/sources.list.d/oneAPI.list

ARG DPCPP_VER
ARG MKL_VER
ARG CCL_VER

RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
    intel-oneapi-runtime-dpcpp-cpp=${DPCPP_VER} \
    intel-oneapi-runtime-mkl=${MKL_VER} \
    intel-oneapi-runtime-ccl=${CCL_VER} && \
    apt-get clean && \
    rm -rf  /var/lib/apt/lists/*

WORKDIR /
COPY xpu-requirements.txt .

RUN python -m pip --no-cache-dir install -r xpu-requirements.txt

ADD https://raw.githubusercontent.com/intel/intel-extension-for-tensorflow/master/third-party-programs/dockerlayer/THIRD-PARTY-PROGRAMS.txt /licenses/
ADD https://raw.githubusercontent.com/intel/intel-extension-for-tensorflow/master/third-party-programs/dockerlayer/third-party-program-of-intel-extension-for-tensorflow.txt /licenses/
ADD https://raw.githubusercontent.com/intel/intel-extension-for-tensorflow/master/third-party-programs/dockerlayer/third-party-programs-of-intel-tensorflow.txt /licenses/
ADD https://raw.githubusercontent.com/intel/intel-extension-for-tensorflow/master/third-party-programs/dockerlayer/third-party-programs-of-intel-optimization-for-horovod.txt /licenses/

ENV LD_LIBRARY_PATH=/opt/intel/oneapi/redist/lib:$LD_LIBRARY_PATH

FROM ${PYTHON_BASE} AS itex-xpu-base-idp

RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
    apt-utils \
    build-essential \
    clinfo \
    git \
    gnupg2 \
    gpg-agent \
    rsync \
    unzip \
    wget && \
    apt-get clean && \
    rm -rf  /var/lib/apt/lists/*

ARG ICD_VER
ARG LEVEL_ZERO_GPU_VER
ARG LEVEL_ZERO_VER
ARG LEVEL_ZERO_DEV_VER

RUN no_proxy="" NO_PROXY="" wget -qO - https://repositories.intel.com/gpu/intel-graphics.key | \
    gpg --dearmor --output /usr/share/keyrings/intel-graphics.gpg
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/intel-graphics.gpg] https://repositories.intel.com/gpu/ubuntu jammy/lts/2350 unified" | \
    tee /etc/apt/sources.list.d/intel-gpu-jammy.list

RUN no_proxy="" NO_PROXY="" apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
    intel-opencl-icd=${ICD_VER} \
    intel-level-zero-gpu=${LEVEL_ZERO_GPU_VER} \
    level-zero=${LEVEL_ZERO_VER} \
    level-zero-dev=${LEVEL_ZERO_DEV_VER} && \
    apt-get clean && \
    rm -rf  /var/lib/apt/lists/*

ARG TF_VER="2.15.0"

RUN conda install intel-extension-for-tensorflow=${TF_VER}=*xpu* \
    -c intel/label/oneapi -c intel -c conda-forge

ENV LD_LIBRARY_PATH=/opt/conda/envs/idp/lib:$LD_LIBRARY_PATH

ADD https://raw.githubusercontent.com/intel/intel-extension-for-tensorflow/master/third-party-programs/dockerlayer/THIRD-PARTY-PROGRAMS.txt /licenses/
ADD https://raw.githubusercontent.com/intel/intel-extension-for-tensorflow/master/third-party-programs/dockerlayer/third-party-program-of-intel-extension-for-tensorflow.txt /licenses/
ADD https://raw.githubusercontent.com/intel/intel-extension-for-tensorflow/master/third-party-programs/dockerlayer/third-party-programs-of-intel-tensorflow.txt /licenses/
ADD https://raw.githubusercontent.com/intel/intel-extension-for-tensorflow/master/third-party-programs/dockerlayer/third-party-programs-of-intel-optimization-for-horovod.txt /licenses/

FROM itex-xpu-base-${PACKAGE_OPTION} AS itex-xpu-jupyter

WORKDIR /jupyter
COPY jupyter-requirements.txt .
RUN python -m pip install --no-cache-dir -r jupyter-requirements.txt

RUN mkdir -p /jupyter/ && chmod -R a+rwx /jupyter/
RUN mkdir /.local && chmod a+rwx /.local
COPY notebooks/itex/itex-xpu.ipynb /jupyter/xpu.ipynb

EXPOSE 8888

CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter notebook --notebook-dir=/jupyter --port 8888 --ip 0.0.0.0 --no-browser --allow-root --ServerApp.token= --ServerApp.password= --ServerApp.allow_origin=* --ServerApp.base_url=$NB_PREFIX"]
