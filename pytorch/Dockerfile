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

ARG PACKAGE_OPTION=pip

ARG COMPOSE_PROJECT_NAME
FROM ${COMPOSE_PROJECT_NAME}-python AS ipex-base-pip

ARG IPEX_VERSION
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

FROM ${COMPOSE_PROJECT_NAME}-python AS ipex-base-idp

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

FROM ipex-base-${PACKAGE_OPTION} AS jupyter

RUN python -m pip install --no-cache-dir jupyterlab jupyterhub notebook jupyter-server-proxy

RUN mkdir -p /jupyter/ && chmod -R a+rwx /jupyter/
RUN mkdir /.local && chmod a+rwx /.local
WORKDIR /jupyter

ARG PORT=8888
EXPOSE $PORT

CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter notebook --notebook-dir=/jupyter --port $PORT --ip 0.0.0.0 --no-browser --allow-root"]

FROM ipex-base-${PACKAGE_OPTION} AS mlflow

RUN python -m pip install --no-cache-dir mlflow

ARG PORT=5000
EXPOSE $PORT

CMD ["mlflow", "server", "-h", "0.0.0.0", "-p", $PORT]

FROM ipex-base-${PACKAGE_OPTION} AS multinode

RUN apt-get update -y && apt-get install -y --no-install-recommends --fix-missing \
    python3-dev \
    gcc \
    libgl1-mesa-glx \
    libglib2.0-0 \
    virtualenv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ARG INC_VERSION
ARG ONECCL_VERSION

ENV SIGOPT_PROJECT=.

RUN python -m pip install --no-cache-dir oneccl_bind_pt${ONECCL_VERSION:+==${ONECCL_VERSION}} \
    -f https://developer.intel.com/ipex-whl-stable-cpu \
    neural-compressor${INC_VER:+==${INC_VER}}

RUN mkdir -p /licensing

RUN curl --insecure https://raw.githubusercontent.com/oneapi-src/oneCCL/b7d66de16e17f88caffd7c6df4cd5e12b266af84/third-party-programs.txt -o /licensing/oneccl_third_party_programs.txt && \
    curl --insecure https://raw.githubusercontent.com/intel/neural-compressor/master/docker/third-party-programs-pytorch.txt -o /licensing/third-party-programs-pytorch.txt && \
    curl --insecure https://raw.githubusercontent.com/intel/neural-compressor/master/LICENSE -o /licensing/LICENSE

FROM multinode AS multinode-pip

RUN apt-get install -y --no-install-recommends --fix-missing virtualenv

RUN virtualenv --system-site-packages inc && echo "source /inc/bin/activate" > ~/.bashrc

FROM multinode AS multinode-idp 

FROM ${COMPOSE_PROJECT_NAME}-python AS ipex-xpu-base

RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
    apt-utils \
    build-essential \
    clinfo \
    curl \
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
ARG TORCH_VERSION
ARG TORCHVISION_VERSION
ARG IPEX_VERSION
ARG ONECCL_BIND_PT_VERSION
ARG TORCH_WHL_URL

RUN no_proxy=$no_proxy wget -qO - https://repositories.intel.com/graphics/intel-graphics.key | \
    gpg --dearmor --output /usr/share/keyrings/intel-graphics.gpg
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/intel-graphics.gpg] https://repositories.intel.com/graphics/ubuntu jammy max" | \
    tee  /etc/apt/sources.list.d/intel.gpu.jammy.list

RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
    intel-opencl-icd=${ICD_VER} \
    intel-level-zero-gpu=${LEVEL_ZERO_GPU_VER} \
    level-zero=${LEVEL_ZERO_VER} \
    level-zero-dev=${LEVEL_ZERO_DEV_VER} && \
    apt-get clean && \
    rm -rf  /var/lib/apt/lists/*

RUN no_proxy=$no_proxy wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB \
   | gpg --dearmor | tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null && \
   echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" \
   | tee /etc/apt/sources.list.d/oneAPI.list

RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
    intel-oneapi-runtime-dpcpp-cpp=${DPCPP_VER} \
    intel-oneapi-runtime-mkl=${MKL_VER} \
    intel-oneapi-runtime-ccl=${CCL_VER};

RUN python -m pip install torch==${TORCH_VERSION} -f ${TORCH_WHL_URL} && \
    python -m pip install intel_extension_for_pytorch==${IPEX_VERSION} -f ${TORCH_WHL_URL} && \
    python -m pip install torchvision==${TORCHVISION_VERSION} -f ${TORCH_WHL_URL} && \
    python -m pip install oneccl_bind_pt==${ONECCL_BIND_PT_VERSION} -f ${TORCH_WHL_URL};

ENV LD_LIBRARY_PATH=/opt/intel/oneapi/lib:/opt/intel/oneapi/lib/intel64:$LD_LIBRARY_PATH

ARG UNAME=user
ARG GID=109
ARG GNAME=render
ARG VNAME=video

RUN useradd -m -s /bin/bash $UNAME

RUN groupadd -g $GID $GNAME

RUN usermod -a -G $VNAME,$GNAME $UNAME

USER user

FROM ipex-xpu-base AS ipex-xpu-jupyter

USER root

RUN python -m pip install --no-cache-dir jupyterlab jupyterhub notebook jupyter-server-proxy 

USER user

RUN if [ ! -d $(which conda) ]; then \
    echo "conda activate idp" >> ~/.bashrc; \
    fi

RUN mkdir -p ~/jupyter/ && chmod -R a+rwx ~/jupyter/

WORKDIR /~/jupyter
COPY --chown=user notebooks/ipex/ipex-xpu.ipynb /~/jupyter/xpu.ipynb

ARG PORT=8888
EXPOSE $PORT

CMD ["bash", "-c", "python -m jupyter notebook --notebook-dir=/~/jupyter --port $PORT --ip 0.0.0.0 --no-browser --allow-root"]

FROM ${COMPOSE_PROJECT_NAME}-python as torchserve-base

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

COPY serving/requirements.txt requirements.txt

RUN python -m pip install --no-cache-dir -U pip setuptools && \
    python -m pip install --no-cache-dir -r requirements.txt

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
