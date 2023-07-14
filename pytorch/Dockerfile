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
ENV LANG C.UTF-8
ARG PYTHON_VERSION

SHELL ["/bin/bash", "-c"]

RUN apt-get update -y && \
    apt-cache search libxml2 && \
    apt-get install -y --no-install-recommends --fix-missing \
    ca-certificates \
    curl \
    wget
    # libxml2-dev

ARG IPEX_VERSION

FROM base AS ipex-base-pip

RUN apt-get install -y --no-install-recommends --fix-missing \
    python${PYTHON_VERSION} \
    python3-pip

# Some TF tools expect a "python" binary
RUN ln -s $(which python${PYTHON_VERSION}) /usr/local/bin/python

RUN python -m pip --no-cache-dir install --upgrade \
    pip \
    setuptools \
    psutil

ARG PYTORCH_VERSION
ARG TORCHAUDIO_VERSION
ARG TORCHVISION_VERSION

RUN python -m pip install --no-cache-dir \
    torch==${PYTORCH_VERSION} \
    torchvision==${TORCHVISION_VERSION} \
    torchaudio==${TORCHAUDIO_VERSION} \
    -f https://download.pytorch.org/whl/cpu/torch_stable.html \
    intel_extension_for_pytorch==${IPEX_VERSION}+cpu \
    -f https://developer.intel.com/ipex-whl-stable-cpu

RUN mkdir -p /licensing && \
	wget -O - https://github.com/intel/intel-extension-for-pytorch/archive/v${IPEX_VERSION}+cpu.tar.gz | \
	tar -xz -C /licensing --strip=2 "intel-extension-for-pytorch-${IPEX_VERSION}-cpu/third-party-programs/"

FROM idp-core AS ipex-base-idp

ARG IPEX_VERSION
ARG PYTORCH_VERSION
ARG TORCHAUDIO_VERSION
ARG TORCHVISION_VERSION

RUN conda run -n idp python -m pip install --no-cache-dir \
    setuptools \
    psutil \
    torch==${PYTORCH_VERSION} \
    torchvision==${TORCHVISION_VERSION} \
    torchaudio==${TORCHAUDIO_VERSION} \
    -f https://download.pytorch.org/whl/cpu/torch_stable.html \
    intel_extension_for_pytorch==${IPEX_VERSION}+cpu \
    -f https://developer.intel.com/ipex-whl-stable-cpu && \
    apt-get clean && conda clean -y --all

RUN echo "conda activate idp" >> ~/.bashrc

RUN ln -sf /root/conda/envs/idp/bin/python /usr/local/bin/python && \
    ln -sf /root/conda/envs/idp/bin/python /usr/local/bin/python3 && \
    ln -sf /root/conda/envs/idp/bin/python /usr/bin/python

RUN mkdir -p /licensing && \
	wget -O - https://github.com/intel/intel-extension-for-pytorch/archive/v${IPEX_VERSION}+cpu.tar.gz | \
	tar -xz -C /licensing --strip=2 "intel-extension-for-pytorch-${IPEX_VERSION}-cpu/third-party-programs/"

FROM ipex-base-${PACKAGE_OPTION} AS jupyter

RUN python -m pip install --no-cache-dir jupyter matplotlib jupyter_http_over_ws ipykernel nbformat
RUN python -m jupyter serverextension enable --py jupyter_http_over_ws

RUN mkdir -p /jupyter/ && chmod -R a+rwx /jupyter/
RUN mkdir /.local && chmod a+rwx /.local
WORKDIR /jupyter

ARG PORT=8888
EXPOSE $PORT

RUN python -m ipykernel.kernelspec

CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter notebook --notebook-dir=/jupyter --port $PORT --ip 0.0.0.0 --no-browser --allow-root"]

FROM ipex-base-${PACKAGE_OPTION} AS mlflow

RUN python -m pip install --no-cache-dir mlflow

ARG PORT=5000
EXPOSE $PORT

CMD ["mlflow", "server", "-h", "0.0.0.0", "-p", $PORT]

FROM ipex-base-${PACKAGE_OPTION} AS inc

RUN apt-get install -y --no-install-recommends --fix-missing \
    python3-dev \
    gcc \
    libgl1-mesa-glx \
    libglib2.0-0

ARG INC_VERSION
ARG ONECCL_VERSION

ENV SIGOPT_PROJECT=.

RUN python -m pip install --no-cache-dir oneccl_bind_pt${ONECCL_VERSION:+==${ONECCL_VERSION}} \
    -f https://developer.intel.com/ipex-whl-stable-cpu \
    neural-compressor${INC_VER:+==${INC_VER}} \
    numpy==1.23.1 

RUN curl https://raw.githubusercontent.com/oneapi-src/oneCCL/b7d66de16e17f88caffd7c6df4cd5e12b266af84/third-party-programs.txt -o /licensing/oneccl_third_party_programs.txt && \
    curl https://raw.githubusercontent.com/intel/neural-compressor/master/docker/third-party-programs-pytorch.txt -o /licensing/third-party-programs-pytorch.txt && \
    curl https://raw.githubusercontent.com/intel/neural-compressor/master/LICENSE -o /licensing/LICENSE

FROM inc AS inc-pip

RUN apt-get install -y --no-install-recommends --fix-missing virtualenv

RUN virtualenv --system-site-packages inc && echo "source /inc/bin/activate" > ~/.bashrc

FROM inc AS inc-idp
