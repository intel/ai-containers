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

ARG BASE_IMAGE=ubuntu
ARG BASE_TAG=22.04

FROM ${BASE_IMAGE}:${BASE_TAG} AS dgpu-base

ENV DEBIAN_FRONTEND=noninteractive

# See http://bugs.python.org/issue19846
ENV LANG C.UTF-8
ARG PYTHON_VERSION

EXPOSE 8080

ENV LANG=C.UTF-8

SHELL ["/bin/bash", "-c"]

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends --fix-missing \
    apt-utils \
    build-essential \
    bzip2 \
    ca-certificates \
    clinfo \
    cmake \
    diffutils \
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
    sudo \
    xz-utils && \
    rm -rf /var/lib/apt/lists/*

# GPU Drivers setup
ARG DEVICE
ARG ICD_VER
ARG LEVEL_ZERO_GPU_VER
ARG LEVEL_ZERO_VER
ARG LEVEL_ZERO_DEV_VER


# Public Drivers link
RUN wget -qO - https://repositories.intel.com/gpu/intel-graphics.key | \
    gpg --dearmor --output /usr/share/keyrings/intel-graphics.gpg
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/intel-graphics.gpg] https://repositories.intel.com/gpu/ubuntu jammy/lts/2350 unified" | \
    tee /etc/apt/sources.list.d/intel-gpu-jammy.list

RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
    intel-opencl-icd="${ICD_VER}" \
    intel-level-zero-gpu="${LEVEL_ZERO_GPU_VER}" \
    level-zero="${LEVEL_ZERO_VER}"

RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
    intel-media-va-driver-non-free \
    libmfx1 \
    libmfxgen1 \
    libvpl2 \
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
    libxatracker2 \
    mesa-va-drivers \
    mesa-vdpau-drivers \
    mesa-vulkan-drivers \
    va-driver-all \
    vainfo \
    hwinfo \
    clinfo

RUN apt-get install -y --no-install-recommends --fix-missing \
    libigc-dev \
    intel-igc-cm \
    libigdfcl-dev \
    libigfxcmrt-dev \
    level-zero-dev="${LEVEL_ZERO_DEV_VER}" && \
    rm -rf /var/lib/apt/lists/*

RUN rm /etc/apt/sources.list.d/*list

FROM dgpu-base as deep-learning-python

# Setting up non-root directories
RUN useradd --uid 1000 -d /home/dev -s /bin/bash dev
RUN groupadd -g 109 render
## Add the user to the required groups
RUN usermod -aG root,sudo,video,render dev
# Set a password for the user (Optional)
RUN echo 'dev:password' | chpasswd
USER dev
WORKDIR /home/dev

ENV CONDA_ROOT=/home/dev/conda

# Miniforge Python Installation
ARG MINIFORGE_VERSION
ARG PYTHON_VERSION
ARG IDP_VERSION
ARG INTEL_CHANNEL

RUN wget --progress=dot:giga --no-check-certificate "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-${MINIFORGE_VERSION}.sh" -O miniforge.sh && \
    chmod +x miniforge.sh && \
    ./miniforge.sh -b -p "${CONDA_ROOT}" && \
    rm ./miniforge.sh && \
    ln -s "${CONDA_ROOT}" "${CONDA_ROOT}/../miniforge3"  && \
    export PATH="${CONDA_ROOT}/bin/:${PATH}" && \
    conda config --add channels ${INTEL_CHANNEL} && \
    conda init --all && \
    conda install -y \
        'colorama==0.4.6' \
        'conda==24.5.0' \
        'jupyter-server-proxy==4.3.0' \
        'jupyterhub==5.0.0' \
        'ld_impl_linux-64==2.40' \
        'mamba==1.5.8' \
        'networkx==3.3' \
        'notebook==7.2.1' \
        'python==3.10.14' \
        && \
    jupyter labextension disable "@jupyterlab/apputils-extension:announcements" && \
    conda clean -y --all

ENV PATH ${CONDA_ROOT}/condabin:${CONDA_ROOT}/bin/:${PATH}
RUN conda config --set pip_interop_enabled True

##############################
# PyTorch cpu Installation
ARG IDP_VERSION
ARG DPNP_VERSION
ARG NUMPY_VERSION
ARG TORCH_CPU_VERSION
ARG ONECCL_CPU_VERSION
ARG IPEX_CPU_VERSION
ARG TORCHVISION_CPU_VERSION
ARG TORCHAUDIO_CPU_VERSION
ARG DEEPSPEED_VERSION

# PyTorch CPU Env - conda packages
RUN conda create -yn pytorch-cpu \
    -c huggingface \
        "python=${PYTHON_VERSION}" \
        'accelerate==0.32.1' \
        "dpnp=${DPNP_VERSION}" \
        "intel-extension-for-pytorch=${IPEX_CPU_VERSION}" \
        'ipykernel==6.29.5' \
        'kernda==0.3.0'  \
        'matplotlib-base>=3.8.4' \
        "oneccl_bind_pt=${ONECCL_CPU_VERSION}" \
        "pytorch=${TORCH_CPU_VERSION}" \
        'tensorboardx==2.6.2.2' \
        "torchaudio=${TORCHAUDIO_CPU_VERSION}" \
        "torchvision=${TORCHVISION_CPU_VERSION}" \
    conda clean -y --all

# PyPI packages
RUN conda run -n pytorch-cpu pip install --no-deps --no-cache-dir \
        'dataset-librarian==1.0.4' \
        && \
    conda run -n pytorch-cpu pip install --no-cache-dir \
        'evaluate==0.4.2' \
        "git+https://github.com/huggingface/optimum-intel.git" \
        && \
    conda clean -y --all

#######################################
# PyTorch GPU Installation
ARG IDP_VERSION
ARG DPNP_VERSION
ARG NUMPY_VERSION
ARG TORCH_XPU_VERSION
ARG ONECCL_XPU_VERSION
ARG IPEX_XPU_VERSION
ARG TORCHVISION_XPU_VERSION
ARG TORCHAUDIO_XPU_VERSION
ARG IDEX_VERSION

# PyTorch GPU Env - conda packages
RUN conda create -yn 'pytorch-gpu' \
    -c huggingface \
        "python=${PYTHON_VERSION}" \
        'accelerate==0.32.1' \
        "dpnp=${DPNP_VERSION}" \
        "intel-extension-for-pytorch=${IPEX_XPU_VERSION}" \
        'ipykernel==6.29.5' \
        'kernda==0.3.0' \
        'matplotlib-base>=3.8.4' \
        "oneccl_bind_pt=${ONECCL_XPU_VERSION}" \
        "pytorch=${TORCH_XPU_VERSION}" \
        'tensorboardx==2.6.2.2' \
        "torchaudio=${TORCHAUDIO_XPU_VERSION}" \
        "torchvision=${TORCHVISION_XPU_VERSION}" \
        && \
    conda clean -y --all

RUN conda run -n 'pytorch-gpu' pip install --no-deps --no-cache-dir \
        'dataset-librarian==1.0.4' \
        && \
    conda run -n 'pytorch-gpu' pip install --no-cache-dir \
        'evaluate==0.4.2' \
        "git+https://github.com/huggingface/optimum-intel.git" \
        && \
    conda clean -y --all

#######################################
# TensorFlow cpu Installation
ARG IDP_VERSION
ARG DPNP_VERSION
ARG NUMPY_VERSION

ARG TF_VERSION
ARG ITEX_CPU_VERSION
ARG ITEX_XPU_VERSION
ARG HOROVOD_VERSION
ARG IMPI_VERSION

ARG HOROVOD_WITH_TENSORFLOW=1
ARG HOROVOD_WITHOUT_MXNET=1
ARG HOROVOD_WITHOUT_GLOO=1
ARG HOROVOD_WITH_MPI=1


# Tensorflow Env - conda packages
RUN conda create -yn 'tensorflow-cpu' \
        "python=${PYTHON_VERSION}" \
        "dpnp=${DPNP_VERSION}" \
        "intel-extension-for-tensorflow=${ITEX_CPU_VERSION}=*cpu*" \
        "intel-optimization-for-horovod=${HOROVOD_VERSION}" \
        'ipykernel==6.29.5' \ 
        'kernda==0.3.0' \
        'matplotlib-base>=3.8.4' \
        'mpi==1.0' \
        'mpich==4.2.2' \
        'onnx==1.14.1' \
        'py-cpuinfo==9.0.0' \
        "tensorflow=${TF_VERSION}" \
        'tensorflow-hub==0.16.1' \
        && \
    conda clean -y --all

RUN conda run -n 'tensorflow-cpu' pip install --no-deps --no-cache-dir \
        'dataset-librarian==1.0.4' \
        && \
    conda clean -y --all

#######################################
# TensorFlow gpu Installation
RUN conda create -yn 'tensorflow-gpu' \
        "python=${PYTHON_VERSION}" \
        "dpnp=${DPNP_VERSION}" \
        "intel-extension-for-tensorflow=${ITEX_XPU_VERSION}=*xpu*" \
        "intel-optimization-for-horovod=${HOROVOD_VERSION}" \
        'ipykernel==6.29.5' \
        'kernda==0.3.0' \
        'matplotlib-base>=3.8.4' \
        'mpi==1.0' \
        'mpich==4.2.2' \
        'onnx==1.14.1' \
        'py-cpuinfo==9.0.0' \
        "tensorflow=${TF_VERSION}" \
        'tensorflow-hub==0.16.1' \
        && \
    conda clean -y --all

RUN conda run -n 'tensorflow-gpu' pip install --no-deps --no-cache-dir \
        'dataset-librarian==1.0.4' \
        && \
    conda clean -y --all

#######################################
# Adding jupyter capabilities

EXPOSE 8888

RUN mkdir -p ~/jupyter/ && chmod -R a+rwx ~/jupyter/ && \
    mkdir ~/.local && chmod a+rwx ~/.local

RUN \
    ENVS_LIST=('pytorch-cpu' 'pytorch-gpu' 'tensorflow-cpu' 'tensorflow-gpu') && \
    KERNEL_NAMES=('Intel PyTorch cpu' 'Intel PyTorch gpu' 'Intel TensorFlow cpu' 'Intel TensorFlow gpu') && \
    for i in "${!ENVS_LIST[@]}"; do \
        CONDA_ENV="${ENVS_LIST[i]}" && \
        KERNEL_NAME="${KERNEL_NAMES[i]}" && \
        KERNEL_DIR="${CONDA_ROOT}/envs/$CONDA_ENV/share/jupyter/kernels/$CONDA_ENV" && \
        conda list -n "$CONDA_ENV" | grep typing_extensions && \
        conda run -n "$CONDA_ENV" python -m ipykernel install --prefix "${CONDA_ROOT}/envs/$CONDA_ENV" --name "$CONDA_ENV" --display-name "$KERNEL_NAME" && \
        conda run -n "$CONDA_ENV" kernda -o -y "$KERNEL_DIR/kernel.json" && \
        conda run -n "$CONDA_ENV" jupyter kernelspec list \
    ; done

CMD ["bash", "-c", "jupyter lab --notebook-dir=~/jupyter --port 8888 --ip 0.0.0.0 --no-browser --allow-root"]

#######################################
# Adding distributed capabilities

FROM deep-learning-base as deep-learning

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

RUN conda install -n pytorch-cpu -c "${INTEL_CHANNEL}" -c conda-forge \
        deepspeed="${DEEPSPEED_VERSION}" \
        'tensorboardx>=2.6.2.2'

RUN ENVS_LIST=('pytorch-cpu' 'pytorch-gpu') && \
    for i in "${!ENVS_LIST[@]}"; do \
        CONDA_ENV="${ENVS_LIST[i]}" && \
        conda install -yn "$CONDA_ENV" \
        "deepspeed=${DEEPSPEED_VERSION}" \
        'tensorboardx==2.6.2.2' \
    ; done && \
    conda clean -y --all

COPY --chown=dev notebooks /home/dev/jupyter
COPY --chown=dev tests /home/dev/sample-tests
