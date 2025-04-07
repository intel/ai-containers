# Copyright (c) 2022 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
#
# This file was assembled from multiple pieces, whose use is documented
# throughout. Please refer to the TensorFlow dockerfiles documentation
# for more information.

# based on https://github.com/pytorch/pytorch/blob/master/Dockerfile
#
# NOTE: To build this you will need a docker version >= 19.03 and DOCKER_BUILDKIT=1
#
#       If you do not use buildkit you are not going to have a good time
#
#       For reference:
#           https://docs.docker.com/develop/develop-images/build_enhancements/

ARG BASE_IMAGE_NAME=ubuntu
ARG BASE_IMAGE_TAG=22.04
ARG PACKAGE_OPTION=pip

FROM ${BASE_IMAGE_NAME}:${BASE_IMAGE_TAG} AS base

# See http://bugs.python.org/issue19846
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8

SHELL ["/bin/bash", "-c"]

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends --fix-missing \
    ca-certificates \
    wget

FROM base AS idp

ARG PYTHON_VERSION
ARG MINIFORGE_VERSION
ARG IDP_VERSION=full

RUN wget --progress=dot:giga --no-check-certificate "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-${MINIFORGE_VERSION}.sh" -O miniforge.sh && \
    chmod +x miniforge.sh && \
    ./miniforge.sh -b -p /opt/conda && \
    rm ./miniforge.sh && \
    ln -s /opt/conda ~/miniforge3 && \
    export PATH="/opt/conda/bin/:${PATH}" && \
    conda update -y conda && \
    conda config --add channels https://software.repos.intel.com/python/conda/ && \
    conda create -yn idp \
    "intelpython3_full" \
    "python=${PYTHON_VERSION}" && \
    conda init --all && \
    apt-get clean && conda clean -y --all && \
    rm -rf /var/lib/apt/lists/*

ENV PATH /opt/conda/envs/idp/bin:/opt/conda/condabin:/opt/conda/bin/:${PATH}
ENV LD_LIBRARY_PATH /lib64/:/usr/lib64/:/usr/local/lib64:/opt/conda/envs/idp/lib:${LD_LIBRARY_PATH}

RUN echo "conda activate idp" >> ~/.bashrc

WORKDIR /
COPY idp-requirements.txt .

RUN conda install -y --file idp-requirements.txt && \
    conda clean -y --all

RUN ln -sf /opt/conda/envs/idp/bin/python /usr/local/bin/python && \
    ln -sf /opt/conda/envs/idp/bin/python /usr/local/bin/python3 && \
    ln -sf /opt/conda/envs/idp/bin/python /usr/bin/python

FROM base AS pip

ARG PYTHON_VERSION

RUN apt-get install -y --no-install-recommends --fix-missing \
    libpython${PYTHON_VERSION} \
    python${PYTHON_VERSION} \
    python3-pip \
    python${PYTHON_VERSION}-distutils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN rm -rf /usr/lib/python${PYTHON_VERSION}/EXTERNALLY-MANAGED

# Some TF tools expect a "python" binary
RUN ln -sf "$(which python${PYTHON_VERSION})" /usr/local/bin/python && \
    ln -sf "$(which python${PYTHON_VERSION})" /usr/local/bin/python3 && \
    ln -sf "$(which python${PYTHON_VERSION})" /usr/bin/python

RUN python -m pip --no-cache-dir install --upgrade pip

WORKDIR /
COPY requirements.txt .

RUN python -m pip --no-cache-dir install -r requirements.txt

FROM ${PACKAGE_OPTION} as xpu-base

RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
        apt-utils \
        build-essential \
        clinfo \
        git \
        gnupg2 \
        gpg-agent \
        rsync \
        unzip && \
    apt-get clean && \
    rm -rf  /var/lib/apt/lists/*

RUN wget -qO - https://repositories.intel.com/gpu/intel-graphics.key | \
    gpg --yes --dearmor --output /usr/share/keyrings/intel-graphics.gpg
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/intel-graphics.gpg] https://repositories.intel.com/gpu/ubuntu jammy unified" | \
    tee /etc/apt/sources.list.d/intel-gpu-jammy.list

ARG ICD_VER
ARG OCLOC_VER
ARG LEVEL_ZERO_VER
ARG LEVEL_ZERO_DEV_VER
ARG XPU_SMI_VER

RUN apt-get update && \
        apt-get install -y --no-install-recommends \
            intel-opencl-icd=${ICD_VER} \
            intel-ocloc=${OCLOC_VER} \
            libze1=${LEVEL_ZERO_VER} \
            libze-dev=${LEVEL_ZERO_DEV_VER} \
            xpu-smi=${XPU_SMI_VER} && \
        apt-get clean && \
        rm -rf  /var/lib/apt/lists/*

RUN rm -rf /etc/apt/sources.list.d/intel-gpu-jammy.list

FROM xpu-base as xpu-base-runtime

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
    rm -rf  /var/lib/apt/lists/*

RUN  rm -rf /etc/apt/sources.list.d/oneAPI.list rm -rf
RUN if eval "which conda >/dev/null"; then \
        echo 'export OCL_ICD_VENDORS="/etc/OpenCL/vendors"' >> ~/.bashrc; \
    fi

FROM xpu-base as xpu-dl-essentials

ARG DL_ESSENTIALS_VER

RUN wget --progress=dot:giga -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | \
        gpg --dearmor | tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | \
        tee /etc/apt/sources.list.d/oneAPI.list

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        intel-deep-learning-essentials=${DL_ESSENTIALS_VER} && \
    apt-get clean && \
    rm -rf  /var/lib/apt/lists/* /etc/apt/sources.list.d/oneAPI.list
