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

FROM ${BASE_IMAGE_NAME}:${BASE_IMAGE_TAG} AS base

# See http://bugs.python.org/issue19846
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8

SHELL ["/bin/bash", "-c"]

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends --fix-missing \
    ca-certificates \
    curl/jammy-updates \
    wget

FROM base AS idp

ARG PYTHON_VERSION
ARG MINICONDA_VERSION
ARG IDP_VERSION=core

RUN wget --no-check-certificate https://repo.anaconda.com/miniconda/Miniconda3-${MINICONDA_VERSION}.sh -O miniconda.sh && \        
    chmod +x miniconda.sh && \
    ./miniconda.sh -b -p /opt/conda && \
    rm ./miniconda.sh && \
    ln -s /opt/conda ~/miniconda3 && \
    export PATH=/opt/conda/bin/:${PATH} && \
    conda update -y conda && \
    conda config --add channels intel && \
    conda create -yn idp intelpython3_${IDP_VERSION} python=${PYTHON_VERSION} && \
    conda init --all && \
    apt-get clean && conda clean -y --all && \
    rm -rf /var/lib/apt/lists/*

ENV PATH /opt/conda/envs/idp/bin:/opt/conda/condabin:/opt/conda/bin/:${PATH}
ENV LD_LIBRARY_PATH /lib64/:/usr/lib64/:/usr/local/lib64:/opt/conda/envs/idp/lib:${LD_LIBRARY_PATH}

RUN echo "conda activate idp" >> ~/.bashrc

RUN conda run -n idp python -m pip install --no-cache-dir numpy==1.22.4

RUN ln -sf /opt/conda/envs/idp/bin/python /usr/local/bin/python && \
    ln -sf /opt/conda/envs/idp/bin/python /usr/local/bin/python3 && \
    ln -sf /opt/conda/envs/idp/bin/python /usr/bin/python

FROM base AS pip

ARG PYTHON_VERSION

RUN apt-get install -y --no-install-recommends --fix-missing \
    python${PYTHON_VERSION} \
    python3-pip \
    python${PYTHON_VERSION}-distutils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN rm -rf /usr/lib/python${PYTHON_VERSION}/EXTERNALLY-MANAGED

# Some TF tools expect a "python" binary
RUN ln -sf $(which python${PYTHON_VERSION}) /usr/local/bin/python && \
    ln -sf $(which python${PYTHON_VERSION}) /usr/local/bin/python3 && \
    ln -sf $(which python${PYTHON_VERSION}) /usr/bin/python

RUN python -m pip --no-cache-dir install --upgrade \
    pip \
    numpy \
    setuptools \
    psutil
