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

ARG REGISTRY
ARG REPO
ARG GITHUB_RUN_NUMBER
ARG BASE_IMAGE_NAME
ARG BASE_IMAGE_TAG
ARG PACKAGE_OPTION=pip
ARG PYTHON_VERSION
ARG PYTHON_BASE=${REGISTRY}/${REPO}:b-${GITHUB_RUN_NUMBER}-${BASE_IMAGE_NAME}-${BASE_IMAGE_TAG}-${PACKAGE_OPTION}-py${PYTHON_VERSION}-base
FROM ${PYTHON_BASE} AS ipex-base-pip

ARG IPEX_VERSION
ARG PYTORCH_VERSION
ARG TORCHAUDIO_VERSION
ARG TORCHVISION_VERSION

WORKDIR /
COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt

FROM ${PYTHON_BASE} AS ipex-base-idp

ARG IPEX_VERSION
ARG PYTORCH_VERSION
ARG TORCHAUDIO_VERSION
ARG TORCHVISION_VERSION

WORKDIR /
COPY requirements.txt .

RUN conda run -n idp python -m pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && conda clean -y --all

FROM ipex-base-${PACKAGE_OPTION} AS jupyter

WORKDIR /jupyter
COPY jupyter-requirements.txt .

RUN python -m pip install --no-cache-dir -r jupyter-requirements.txt

RUN mkdir -p /jupyter/ && chmod -R a+rwx /jupyter/
RUN mkdir /.local && chmod a+rwx /.local

EXPOSE 8888

CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter notebook --notebook-dir=/jupyter --port 8888 --ip 0.0.0.0 --no-browser --allow-root --ServerApp.token= --ServerApp.password= --ServerApp.allow_origin=* --ServerApp.base_url=$NB_PREFIX"]

FROM ipex-base-${PACKAGE_OPTION} AS multinode

RUN apt-get update -y && apt-get install -y --no-install-recommends --fix-missing \
    python3-dev \
    gcc \
    libgl1-mesa-glx \
    libglib2.0-0 \
    virtualenv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV SIGOPT_PROJECT=.

WORKDIR /
COPY multinode-requirements.txt .

RUN python -m pip install --no-cache-dir -r multinode-requirements.txt

ARG PYTHON_VERSION
RUN echo "source /usr/local/lib/python${PYTHON_VERSION}/dist-packages/oneccl_bindings_for_pytorch/env/setvars.sh" >> ~/.bashrc

ENV I_MPI_ROOT=/usr/local/lib/python${PYTHON_VERSION}/dist-packages/oneccl_bindings_for_pytorch
ENV CCL_ROOT=/usr/local/lib/python${PYTHON_VERSION}/dist-packages/oneccl_bindings_for_pytorch
ENV FI_PROVIDER_PATH=/usr/local/lib/python${PYTHON_VERSION}/dist-packages/oneccl_bindings_for_pytorch/opt/mpi/libfabric/lib/prov:/usr/lib64/libfabric
ENV LIBRARY_PATH=/usr/local/lib/python${PYTHON_VERSION}/dist-packages/oneccl_bindings_for_pytorch/lib
ENV LD_LIBRARY_PATH=/usr/local/lib/python${PYTHON_VERSION}/dist-packages/oneccl_bindings_for_pytorch/opt/mpi/libfabric/lib:/usr/local/lib/python${PYTHON_VERSION}/dist-packages/oneccl_bindings_for_pytorch/lib
ENV PATH=/usr/local/lib/python${PYTHON_VERSION}//dist-packages/oneccl_bindings_for_pytorch/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV CPATH=/usr/local/lib/python${PYTHON_VERSION}/dist-packages/oneccl_bindings_for_pytorch/include

RUN mkdir -p /licensing

RUN wget -q  --no-check-certificate https://raw.githubusercontent.com/oneapi-src/oneCCL/b7d66de16e17f88caffd7c6df4cd5e12b266af84/third-party-programs.txt -O /licensing/oneccl_third_party_programs.txt && \
    wget -q  --no-check-certificate https://raw.githubusercontent.com/intel/neural-compressor/master/docker/third-party-programs-pytorch.txt -O /licensing/third-party-programs-pytorch.txt && \
    wget -q  --no-check-certificate https://raw.githubusercontent.com/intel/neural-compressor/master/LICENSE -O /licensing/LICENSE

FROM ${PYTHON_BASE} AS ipex-xpu-base

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
    gpg --dearmor --output /usr/share/keyrings/intel-graphics.gpg
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/intel-graphics.gpg] https://repositories.intel.com/gpu/ubuntu jammy/lts/2350 unified" | \
    tee /etc/apt/sources.list.d/intel-gpu-jammy.list

ARG ICD_VER
ARG LEVEL_ZERO_GPU_VER
ARG LEVEL_ZERO_VER
ARG LEVEL_ZERO_DEV_VER

RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
    intel-opencl-icd=${ICD_VER} \
    intel-level-zero-gpu=${LEVEL_ZERO_GPU_VER} \
    level-zero=${LEVEL_ZERO_VER} \
    level-zero-dev=${LEVEL_ZERO_DEV_VER} && \
    apt-get clean && \
    rm -rf  /var/lib/apt/lists/*

RUN no_proxy=$no_proxy wget -q  -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB \
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
    intel-oneapi-runtime-ccl=${CCL_VER};

WORKDIR /
COPY xpu-requirements.txt .

RUN python -m pip install --no-cache-dir -r xpu-requirements.txt

ENV LD_LIBRARY_PATH=/opt/intel/oneapi/redist/lib:$LD_LIBRARY_PATH

FROM ipex-xpu-base AS ipex-xpu-jupyter

WORKDIR /jupyter
COPY jupyter-requirements.txt .
RUN python -m pip install --no-cache-dir -r jupyter-requirements.txt

RUN if [ ! -d "$(which conda)" ]; then \
    echo "conda activate idp" >> ~/.bashrc; \
    fi

COPY --chown=root notebooks/ipex-xpu.ipynb /jupyter/xpu.ipynb

EXPOSE 8888

CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter notebook --notebook-dir=/jupyter --port 8888 --ip 0.0.0.0 --no-browser --allow-root --ServerApp.token= --ServerApp.password= --ServerApp.allow_origin=* --ServerApp.base_url=$NB_PREFIX"]

FROM ${PYTHON_BASE} as torchserve-base

ENV PYTHONUNBUFFERED=TRUE

RUN apt-get update -y && apt-get install -y --no-install-recommends --fix-missing \
    numactl \
    openjdk-17-jdk && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash model-server && \
    mkdir -p /home/model-server && \
    mkdir -p /home/model-server/tmp && \
    mkdir -p /home/model-server/logs && \
    mkdir -p /home/model-server/model-store && \
    chown -R model-server /home/model-server/

FROM torchserve-base AS compile

RUN apt-get update -y && apt-get install -y --no-install-recommends --fix-missing \
    g++ \
    git \
    wget \
    python3-dev \
    python3-distutils \
    python3-venv && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /home/venv

ENV PATH="/home/venv/bin:$PATH"

WORKDIR /home/model-server
COPY torchserve-requirements.txt .
COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt && \
    python -m pip install --no-cache-dir -r torchserve-requirements.txt

RUN echo -e "#!/bin/bash \n\
set -e \n\
if [[ \"\$1\" = "serve" ]]; then \n\
    shift 1 \n\
    torchserve --start --ts-config /home/model-server/config.properties --workflow-store /home/model-server/wf-store \n\
else \n\
    eval \"\$@\" \n\
fi \n\
tail -f /dev/null" >> /usr/local/bin/dockerd-entrypoint.sh

FROM torchserve-base AS torchserve

USER model-server
WORKDIR /home/model-server

COPY --chown=model-server --from=compile /home/venv /home/venv
COPY --chown=model-server --chmod=755 --from=compile /usr/local/bin/dockerd-entrypoint.sh /usr/local/bin/dockerd-entrypoint.sh
COPY --chown=model-server serving/config.properties /home/model-server/config.properties

ENV PATH="/home/venv/bin:$PATH"
ENV TEMP=/home/model-server/tmp

# 8080/8081/8082 REST and 7070/7071 gRPC
EXPOSE 8080 8081 8082 7070 7071

ENTRYPOINT ["/usr/local/bin/dockerd-entrypoint.sh"]
CMD ["serve"]
