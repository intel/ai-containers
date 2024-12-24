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

RUN python -m pip install --no-cache-dir -r requirements.txt && \
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

FROM ${PYTHON_BASE} AS ipex-xpu-base-wheels

WORKDIR /
COPY xpu-requirements.txt .

RUN python -m pip install --no-cache-dir -r xpu-requirements.txt && \
    rm -rf xpu-requirements.txt

FROM ipex-xpu-base-wheels AS ipex-xpu-jupyter

WORKDIR /jupyter
COPY jupyter-requirements.txt .

RUN python -m pip install --no-cache-dir -r jupyter-requirements.txt

RUN if eval "which conda >/dev/null"; then \
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

ARG PYTHON_VERSION
RUN apt-get update -y && apt-get install -y --no-install-recommends --fix-missing \
    g++ \
    git \
    wget \
    ${PYTHON_VERSION}-venv \
    python3-distutils \
    python3-venv && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /
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
    apt-get install -y --no-install-recommends pciutils 

ARG GID=110

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
