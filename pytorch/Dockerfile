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
ARG TORCHSERVE_BASE=${PYTHON_BASE}
FROM ${PYTHON_BASE} AS ipex-base-pip

WORKDIR /
COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt && \
    rm -rf requirements.txt

FROM ${PYTHON_BASE} AS ipex-base-idp

WORKDIR /
COPY requirements.txt .

RUN conda run -n idp python -m pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && conda clean -y --all

FROM ipex-base-${PACKAGE_OPTION} AS jupyter

WORKDIR /jupyter
COPY jupyter-requirements.txt .

RUN python -m pip install --no-cache-dir -r jupyter-requirements.txt && \
    rm -rf jupyter-requirements.txt

RUN mkdir -p /jupyter/ && chmod -R a+rwx /jupyter/
RUN mkdir /.local && chmod a+rwx /.local

EXPOSE 8888

CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter notebook --notebook-dir=/jupyter --port 8888 --ip 0.0.0.0 --no-browser --allow-root --ServerApp.token= --ServerApp.password= --ServerApp.allow_origin=* --ServerApp.base_url=$NB_PREFIX"]

FROM ipex-base-${PACKAGE_OPTION} AS multinode

RUN apt-get update -y && apt-get install -y --no-install-recommends --fix-missing \
    python3-dev \
    gcc \
    g++ \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libopenmpi-dev \
    numactl \
    virtualenv

ENV SIGOPT_PROJECT=.

WORKDIR /
COPY multinode/requirements.txt requirements.txt

RUN python -m pip install --no-cache-dir -r requirements.txt && \
    DS_BUILD_OPS=1 python -m pip install --no-cache-dir deepspeed==0.14.4 && \
    echo "Y" | pip uninstall nvidia-ml-py && \
    rm -rf requirements.txt

ENV LD_LIBRARY_PATH="/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH}:/usr/local/lib/python${PYTHON_VERSION}/dist-packages/oneccl_bindings_for_pytorch/opt/mpi/libfabric/lib:/usr/local/lib/python${PYTHON_VERSION}/dist-packages/oneccl_bindings_for_pytorch/lib"

RUN apt-get install -y --no-install-recommends --fix-missing \
    openssh-client \
    openssh-server && \
    rm /etc/ssh/ssh_host_*_key \
    /etc/ssh/ssh_host_*_key.pub && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/run/sshd

ARG PYTHON_VERSION

COPY multinode/generate_ssh_keys.sh /generate_ssh_keys.sh

# modify generate_ssh_keys to be a helper script
# print how to use helper script on bash startup
# Avoids loop for further execution of the startup file
ARG PACKAGE_OPTION=pip
ARG PYPATH="/usr/local/lib/python${PYTHON_VERSION}/dist-packages"
RUN if [ "${PACKAGE_OPTION}" = "idp" ]; then PYPATH="/opt/conda/envs/idp/lib/python${PYTHON_VERSION}/site-packages"; fi && \
    echo "source ${PYPATH}/oneccl_bindings_for_pytorch/env/setvars.sh" >> ~/.startup && \
    cat '/generate_ssh_keys.sh' >> ~/.startup && \
    rm -rf /generate_ssh_keys.sh

COPY multinode/dockerd-entrypoint.sh /usr/local/bin/dockerd-entrypoint.sh
COPY multinode/sshd_config /etc/ssh/sshd_config
COPY multinode/ssh_config /etc/ssh/ssh_config

RUN mkdir -p /licensing

RUN wget -q  --no-check-certificate https://raw.githubusercontent.com/oneapi-src/oneCCL/b7d66de16e17f88caffd7c6df4cd5e12b266af84/third-party-programs.txt -O /licensing/oneccl_third_party_programs.txt && \
    wget -q  --no-check-certificate https://raw.githubusercontent.com/intel/neural-compressor/master/docker/third-party-programs-pytorch.txt -O /licensing/third-party-programs-pytorch.txt && \
    wget -q  --no-check-certificate https://raw.githubusercontent.com/intel/neural-compressor/master/LICENSE -O /licensing/LICENSE

ENTRYPOINT ["/usr/local/bin/dockerd-entrypoint.sh"]

FROM multinode AS hf-genai

COPY hf-genai-requirements.txt .

RUN python -m pip install --no-cache-dir -r hf-genai-requirements.txt && \
    rm -rf hf-genai-requirements.txt

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
    gpg --dearmor --yes --output /usr/share/keyrings/intel-graphics.gpg
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/intel-graphics.gpg] https://repositories.intel.com/gpu/ubuntu jammy unified" | \
    tee /etc/apt/sources.list.d/intel-gpu-jammy.list

ARG ICD_VER
ARG LEVEL_ZERO_GPU_VER
ARG LEVEL_ZERO_VER
ARG LEVEL_ZERO_DEV_VER

RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
    intel-opencl-icd=${ICD_VER} \
    intel-level-zero-gpu=${LEVEL_ZERO_GPU_VER} \
    libze1=${LEVEL_ZERO_VER} \
    libze-dev=${LEVEL_ZERO_DEV_VER} && \
    apt-get clean && \
    rm -rf  /var/lib/apt/lists/*

RUN rm -rf /etc/apt/sources.list.d/intel-gpu-jammy.list

ENV OCL_ICD_VENDORS=/etc/OpenCL/vendors

FROM ipex-xpu-base AS ipex-xpu-base-wheels-pip

WORKDIR /
COPY xpu-requirements.txt .

RUN python -m pip install --no-cache-dir -r xpu-requirements.txt && \
    rm -rf xpu-requirements.txt

FROM ipex-xpu-base AS ipex-xpu-base-wheels-idp

WORKDIR /
COPY xpu-requirements.txt .

RUN conda run -n idp python -m pip install --no-cache-dir -r xpu-requirements.txt && \
    rm -rf xpu-requirements.txt

FROM ipex-xpu-base-wheels-${PACKAGE_OPTION} AS ipex-xpu-jupyter

WORKDIR /jupyter
COPY jupyter-requirements.txt .
RUN python -m pip install --no-cache-dir -r jupyter-requirements.txt

RUN if eval "which conda >/dev/null )"; then \
        echo "conda activate idp" >> ~/.bashrc; \
    fi

COPY --chown=root notebooks/ipex-xpu.ipynb /jupyter/xpu.ipynb

EXPOSE 8888

CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter notebook --notebook-dir=/jupyter --port 8888 --ip 0.0.0.0 --no-browser --allow-root --ServerApp.token= --ServerApp.password= --ServerApp.allow_origin=* --ServerApp.base_url=$NB_PREFIX"]


FROM ${TORCHSERVE_BASE} as torchserve-base

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

RUN apt-get update -y && apt-get install -y --no-install-recommends --fix-missing \
    g++ \
    git \
    wget \
    python3-dev \
    python3-distutils \
    python3-venv && \
    rm -rf /var/lib/apt/lists/*

COPY venv-requirements.txt .

RUN python3 -m venv /home/venv && \
    /home/venv/bin/python -m pip install --no-cache-dir --upgrade pip && \
    /home/venv/bin/python -m pip install --no-cache-dir -r venv-requirements.txt && \
    rm -rf venv-requirements.txt

ENV PATH="/home/venv/bin:$PATH"

WORKDIR /home/model-server

RUN echo -e "#!/bin/bash \n\
set -e \n\
if [[ \"\$1\" = "serve" ]]; then \n\
    shift 1 \n\
    torchserve --start --ts-config /home/model-server/config.properties --workflow-store /home/model-server/wf-store \n\
else \n\
    eval \"\$@\" \n\
fi \n\
tail -f /dev/null" >> /usr/local/bin/dockerd-entrypoint.sh

FROM torchserve-base AS compile-cpu

COPY serving/torchserve-requirements.txt .
COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt && \
    python -m pip install --no-cache-dir -r torchserve-requirements.txt && \
    rm -rf requirements.txt torchserve-requirements.txt

FROM torchserve-base AS compile-xpu

COPY serving/torchserve-xpu-requirements.txt .

RUN python -m pip install --no-cache-dir -r torchserve-xpu-requirements.txt && \
    rm -rf torchserve-xpu-requirements.txt

FROM torchserve-base AS torchserve-cpu

USER model-server
WORKDIR /home/model-server

COPY --chown=model-server --from=compile-cpu /home/venv /home/venv
COPY --chown=model-server --chmod=755 --from=compile-cpu /usr/local/bin/dockerd-entrypoint.sh /usr/local/bin/dockerd-entrypoint.sh
COPY --chown=model-server serving/config.properties /home/model-server/config.properties

ENV PATH="/home/venv/bin:$PATH"
ENV TEMP=/home/model-server/tmp

# 8080/8081/8082 REST and 7070/7071 gRPC
EXPOSE 8080 8081 8082 7070 7071

ENTRYPOINT ["/usr/local/bin/dockerd-entrypoint.sh"]
CMD ["serve"]

FROM torchserve-base AS torchserve-xpu

RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
        gnupg2 \
        gpg-agent \
        rsync && \
    apt-get clean && \
    rm -rf  /var/lib/apt/lists/*

RUN wget -qO - https://repositories.intel.com/gpu/intel-graphics.key | \
    gpg --dearmor --yes --output /usr/share/keyrings/intel-graphics.gpg
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/intel-graphics.gpg] https://repositories.intel.com/gpu/ubuntu jammy unified" | \
    tee /etc/apt/sources.list.d/intel-gpu-jammy.list

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        jq \
        curl \
        libnl-genl-3-200 \
        intel-gsc \
        libdrm2 \
        intel-metrics-discovery \
        intel-metrics-library && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

ARG XPU_SMI_VERSION

ARG API_URL=https://api.github.com/repos/intel/xpumanager/releases/tags/V${XPU_SMI_VERSION}

RUN wget -q --header="Accept: application/vnd.github.v3+json" --header="User-Agent: MyClient/1.0.0" -O - "$API_URL" | tee /tmp/asset_data.txt && \
    wget -q --no-check-certificate "$(jq -r '.assets[] | select(.name | test("^xpu-smi.*u22\\.04_amd64\\.deb$")) | .browser_download_url' < /tmp/asset_data.txt)" && \
    ldconfig && dpkg -i --force-all -- *.deb && \
    rm -rf -- *.deb /etc/apt/sources.list.d/intel-gpu-jammy.list /etc/apt/sources.list.d/oneAPI.list /tmp/asset_data.txt

ARG GID=109

RUN groupadd -g ${GID} render &&\
    usermod -aG video,render model-server

USER model-server

WORKDIR /home/model-server

RUN wget --progress=dot:giga https://raw.githubusercontent.com/pytorch/serve/master/examples/intel_extension_for_pytorch/intel_gpu_metric_collector.py && \
    wget --progress=dot:giga https://raw.githubusercontent.com/pytorch/serve/master/examples/intel_extension_for_pytorch/intel_gpu.py

COPY --chown=model-server --from=compile-xpu /home/venv /home/venv
COPY --chown=model-server --chmod=755 --from=compile-xpu /usr/local/bin/dockerd-entrypoint.sh /usr/local/bin/dockerd-entrypoint.sh
COPY --chown=model-server serving/config-xpu.properties /home/model-server/config.properties

ENV PATH="/home/venv/bin:$PATH"
ENV TEMP=/home/model-server/tmp

# 8080/8081/8082 REST and 7070/7071 gRPC
EXPOSE 8080 8081 8082 7070 7071

ENTRYPOINT ["/usr/local/bin/dockerd-entrypoint.sh"]
CMD ["serve"]
