# Copyright (c) 2024 Intel Corporation
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

# ERASE COMMENTS FROM HERE

ARG BASE_IMAGE=ubuntu
ARG BASE_TAG=22.04

FROM ${BASE_IMAGE}:${BASE_TAG} AS deep-learning-base

SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND=noninteractive
# See http://bugs.python.org/issue19846
ENV LANG C.UTF-8
ARG PYTHON_VERSION

EXPOSE 8080

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends --fix-missing \
        apt-utils \
        build-essential \
        bzip2 \
        ca-certificates \
        cmake \
        g++ \
        gcc \
        git \
        gnupg2 \
        gpg-agent \
        gzip \
        make \
        numactl \
        patch \
        rsync \
        unzip \
        wget \
        xz-utils \
    && \
    rm -rf /var/lib/apt/lists/*

###############################
# GPU Drivers setup
ARG DEVICE
ARG ICD_VER
ARG LEVEL_ZERO_GPU_VER
ARG LEVEL_ZERO_VER
ARG LEVEL_ZERO_DEV_VER

# Public Drivers link
RUN wget -qO - https://repositories.intel.com/gpu/intel-graphics.key | \
    gpg --dearmor --output /usr/share/keyrings/intel-graphics.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/intel-graphics.gpg] https://repositories.intel.com/gpu/ubuntu jammy/lts/2350 unified" | \
    tee /etc/apt/sources.list.d/intel-gpu-jammy.list

RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
        intel-level-zero-gpu="${LEVEL_ZERO_GPU_VER}" \
        intel-opencl-icd="${ICD_VER}" \
        level-zero="${LEVEL_ZERO_VER}"

RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
        clinfo \
        hwinfo \
        intel-media-va-driver-non-free \
        libegl-mesa0 \
        libegl1-mesa \
        libegl1-mesa-dev \
        libgbm1 \
        libgl1-mesa-dev \
        libgl1-mesa-dri \
        libglapi-mesa \
        libgles2-mesa-dev \
        libglx-mesa0 \
        libigdgmm12 \
        libmfx1 \
        libmfxgen1 \
        libvpl2 \
        mesa-va-drivers \
        mesa-vdpau-drivers \
        mesa-vulkan-drivers \
        va-driver-all \
        vainfo

RUN apt-get install -y --no-install-recommends --fix-missing \
        intel-igc-cm \
        libigc-dev \
        libigdfcl-dev \
        libigfxcmrt-dev \
        level-zero-dev="${LEVEL_ZERO_DEV_VER}" \
    && \
    rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*list

##########################
# Setting up non-root directories
RUN useradd --uid 1000 -d /home/dev -s /bin/bash dev
RUN groupadd -g 109 render
## Add the user to the required groups
RUN usermod -aG root,video,render dev
# Set a password for the user (Optional)
# RUN echo 'dev:password' | chpasswd
USER dev
WORKDIR /home/dev

ENV CONDA_ROOT=/home/dev/conda
ARG MINIFORGE_VERSION
ARG PYTHON_VERSION
ARG IDP_VERSION
ARG INTEL_CHANNEL

RUN wget --progress=dot:giga --no-check-certificate "https://github.com/conda-forge/miniforge/releases/latest/download/${MINIFORGE_VERSION}.sh" -O miniforge.sh && \
    chmod +x miniforge.sh && \
    ./miniforge.sh -b -p "${CONDA_ROOT}" && \
    rm ./miniforge.sh && \
    ln -s "${CONDA_ROOT}" "${CONDA_ROOT}/../miniforge"  && \
    export PATH="${CONDA_ROOT}/bin/:${PATH}" && \
    conda init --all && \
    conda update -y conda && \
    conda install -y \
        'jupyterlab>=4.2.6' \
        'notebook>=7.1.3' \
        'nb_conda_kernels>=2.5.1' \
        'urllib3>=2.5.0' \
        'requests>=2.32.4' \
    && \
    jupyter labextension disable "@jupyterlab/apputils-extension:announcements" \
    && \
    conda clean -y --all \
    && \
    conda config --add channels ${INTEL_CHANNEL}

ENV PATH ${CONDA_ROOT}/condabin:${CONDA_ROOT}/bin/:${PATH}

# Improve interoperabilty among conda an pypi packages
RUN conda config --set pip_interop_enabled True

COPY requirements.txt .
RUN python -m pip install --no-cache-dir \
    --ignore-installed -r requirements.txt
RUN rm -rf requirements.txt

#######################################
# PyTorch Installation
ARG IDP_VERSION
ARG DPNP_VERSION
ARG NUMPY_VERSION
ARG TORCH_XPU_VERSION
ARG ONECCL_XPU_VERSION
ARG IPEX_XPU_VERSION
ARG TORCHVISION_XPU_VERSION
ARG TORCHAUDIO_XPU_VERSION
ARG IDEX_VERSION
ARG ONNXRUNTIME_VERSION
ARG NEURAL_COMPRESSOR_VERSION
RUN conda create -yn 'pytorch-gpu' \
    -c huggingface \
        "python=${PYTHON_VERSION}" \
        'accelerate==0.32.1' \
        "dpnp=${DPNP_VERSION}" \
        "intel-extension-for-pytorch=${IPEX_XPU_VERSION}" \
        "neural-compressor=${NEURAL_COMPRESSOR_VERSION}" \
        'ipykernel>=6.29.5' \
        'kernda>=0.3.0' \
        'matplotlib-base>=3.8.4' \
        "oneccl_bind_pt=${ONECCL_XPU_VERSION}" \
        "pytorch=${TORCH_XPU_VERSION}" \
        'tensorboardx>=2.6.2.2' \
        "torchaudio=${TORCHAUDIO_XPU_VERSION}" \
        "torchvision=${TORCHVISION_XPU_VERSION}" \
        "deepspeed=${DEEPSPEED_VERSION}" \
        'tensorboardx=2.6.2.2' \
        && \
    conda clean -y --all


COPY venv_requirements.txt .
RUN conda run -n 'pytorch-gpu' python -m pip install --no-cache-dir -r venv_requirements.txt && \
    conda clean -y --all
RUN rm -rf venv_requirements.txt

#######################################
# Adding jupyter capabilities
EXPOSE 8888

RUN mkdir -p ~/jupyter/ && chmod -R a+rwx ~/jupyter/ && \
    mkdir ~/.local && chmod a+rwx ~/.local

RUN CONDA_ENV="pytorch-gpu" && \
    KERNEL_NAME="PyTorch GPU" && \
    KERNEL_DIR="${CONDA_ROOT}/share/jupyter/kernels/$CONDA_ENV" && \
    conda run -n "$CONDA_ENV" python -m ipykernel install --prefix "$CONDA_ROOT" --name "$CONDA_ENV" --display-name "$KERNEL_NAME" && \
    conda run -n "$CONDA_ENV" kernda -o -y "$KERNEL_DIR/kernel.json" && \
    conda run -n base jupyter kernelspec list

CMD ["bash", "-c", "source activate pytorch-gpu && jupyter lab --notebook-dir=~/jupyter --port 8888 --ip 0.0.0.0 --no-browser --allow-root"]

#######################################
# Adding distributed capabilities
FROM deep-learning-base as deep-learning

SHELL ["/bin/bash", "-c"]
USER root

# Install OpenMPI
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends --fix-missing \
        libopenmpi-dev \
        openmpi-bin \
        openmpi-common

ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
ENV OMPI_MCA_tl_tcp_if_exclude="lo,docker0"

# Install OpenSSH
RUN apt-get install -y --no-install-recommends --fix-missing \
        openssh-client \
        openssh-server \
    && \
    rm -rf \
        /etc/ssh/ssh_host_*_key \
        /etc/ssh/ssh_host_*_key.pub \
        /var/lib/apt/lists/* \
    && \
    mkdir -p /var/run/sshd \
    && \
    echo 'LoginGraceTime 0' >> /etc/ssh/sshd_config

# https://github.com/openucx/ucx/issues/4742#issuecomment-584059909
ENV UCX_TLS=ud,sm,self

USER dev

COPY --chown=dev notebooks /home/dev/jupyter
COPY --chown=dev tests /home/dev/sample-tests

ENV BASH_ENV ~/.bash_profile
RUN echo "conda activate pytorch-gpu" >> ~/.bashrc
