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

ARG BASE_IMAGE_NAME=${BASE_IMAGE_NAME}
ARG BASE_IMAGE_TAG=${BASE_IMAGE_TAG}
FROM ${BASE_IMAGE_NAME}:${BASE_IMAGE_TAG} AS xpu-base

RUN wget -q -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor | tee /usr/share/keyrings/intel-oneapi-archive-keyring.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/intel-oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main " | tee /etc/apt/sources.list.d/oneAPI.list && \
    chmod 644 /usr/share/keyrings/intel-oneapi-archive-keyring.gpg && \
    rm /etc/apt/sources.list.d/intel-graphics.list && \
    wget -q -O- https://repositories.intel.com/graphics/intel-graphics.key | gpg --dearmor | tee /usr/share/keyrings/intel-graphics.gpg > /dev/null && \
    echo "deb [arch=amd64,i386 signed-by=/usr/share/keyrings/intel-graphics.gpg] https://repositories.intel.com/graphics/ubuntu jammy arc" | tee /etc/apt/sources.list.d/intel.gpu.jammy.list && \
    chmod 644 /usr/share/keyrings/intel-graphics.gpg

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends --fix-missing \
    git \
    # libsndfile1 \
    # lsb-release \
    numactl \
    python3 \
    python3-dev \
    python3-pip

RUN ln -sf "$(which python3)" /usr/local/bin/python && \
    ln -sf "$(which python3)" /usr/bin/python

FROM xpu-base AS jax-base

WORKDIR /
COPY requirements.txt .

RUN python -m pip install --no-cache-dir \
    --ignore-installed -r requirements.txt && \
    rm -rf requirements.txt

FROM jax-base AS jupyter

WORKDIR /jupyter
COPY jupyter-requirements.txt .

RUN python -m pip install --no-cache-dir -r jupyter-requirements.txt && \
    rm -rf jupyter-requirements.txt

RUN mkdir -p /jupyter/ && chmod -R a+rwx /jupyter/
RUN mkdir /.local && chmod a+rwx /.local

EXPOSE 8888

CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter notebook --notebook-dir=/jupyter --port 8888 --ip 0.0.0.0 --no-browser --allow-root --ServerApp.token= --ServerApp.password= --ServerApp.allow_origin=* --ServerApp.base_url=$NB_PREFIX"]

FROM jax-base AS jax-multinode

RUN apt-get update -y && apt-get install -y --no-install-recommends --fix-missing \
    # python3-dev \
    gcc \
    # g++ \
    # libgl1-mesa-glx \
    # libglib2.0-0 \
    libopenmpi-dev \
    numactl \
    virtualenv

ENV SIGOPT_PROJECT=. \
    MPI4JAX_USE_SYCL_MPI=1 \
    MPI4PY_BUILD_BACKEND=scikit-build-core

WORKDIR /
COPY multinode/requirements.txt requirements.txt


RUN python -m pip install --no-cache-dir -r requirements.txt && \
    rm -rf requirements.txt

ENV LD_LIBRARY_PATH="/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH}"

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
RUN cat '/generate_ssh_keys.sh' >> ~/.startup && \
    rm -rf /generate_ssh_keys.sh

COPY multinode/dockerd-entrypoint.sh /usr/local/bin/dockerd-entrypoint.sh
COPY multinode/sshd_config /etc/ssh/sshd_config
COPY multinode/ssh_config /etc/ssh/ssh_config

RUN mkdir -p /licensing

ENTRYPOINT ["/usr/local/bin/dockerd-entrypoint.sh"]
