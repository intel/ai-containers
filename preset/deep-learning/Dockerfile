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
    intel-media-va-driver-non-free libmfx1 libmfxgen1 libvpl2 \
    libegl-mesa0 libegl1-mesa libegl1-mesa-dev libgbm1 libgl1-mesa-dev libgl1-mesa-dri \
    libglapi-mesa libgles2-mesa-dev libglx-mesa0 libigdgmm12 libxatracker2 mesa-va-drivers \
    mesa-vdpau-drivers mesa-vulkan-drivers va-driver-all vainfo hwinfo clinfo

RUN apt-get install -y --no-install-recommends --fix-missing \
    libigc-dev intel-igc-cm libigdfcl-dev libigfxcmrt-dev level-zero-dev="${LEVEL_ZERO_DEV_VER}" && \
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
    conda update -y conda && \
    conda config --add channels conda-forge && \
    conda config --add channels intel && \
    conda init --all && \
    conda install -c conda-forge \
        jupyterlab \
        notebook \
        jupyterhub \
        jupyter-server-proxy \
        'mako>=1.2.2' \
        'pyjwt>=2.4.0' \
        'cryptography>=42.0.5' \
        'nodejs>=20.12.2' \
        'idna>=3.7' \
        'tqdm>=4.66.2' \
        && \
    jupyter labextension disable "@jupyterlab/apputils-extension:announcements" && \
    conda clean -y --all

ENV PATH ${CONDA_ROOT}/condabin:${CONDA_ROOT}/bin/:${PATH}

RUN conda config --set pip_interop_enabled True # Improve interoperabilty among conda an pypi packages


# PyTorch Installation
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
RUN conda create -yn pytorch-cpu -c intel/label/oneapi -c "${INTEL_CHANNEL}" -c conda-forge \
        dpnp="${DPNP_VERSION}" \
        numpy="${NUMPY_VERSION}" \
        python="${PYTHON_VERSION}" \
        intel-openmp="${IDP_VERSION}" \
        pytorch="${TORCH_CPU_VERSION}" \
        oneccl_bind_pt="${ONECCL_CPU_VERSION}" \
        intel-extension-for-pytorch="${IPEX_CPU_VERSION}" \
        torchvision="${TORCHVISION_CPU_VERSION}" \
        torchaudio="${TORCHAUDIO_CPU_VERSION}" \
        matplotlib-base \
        ipykernel \
        kernda  \
        'pillow>=10.2.0' \
        'aiohttp>=3.9.0' \
        'tornado>=6.3.3' \
        'jinja2>=3.1.3' \
        'idna>=3.7' \
        onnx \
        && \
    conda clean -y --all

# PyPI packages
RUN conda run -n pytorch-cpu pip install --no-deps --no-cache-dir --ignore-installed \
        ninja \
        python-dotenv \
        'tqdm>=4.66.2' \
        cloud-data-connector \
        dataset-librarian && \
    conda run -n pytorch-cpu pip install --no-cache-dir --ignore-installed \
        transformers \
        datasets \
        evaluate && \
    conda run -n pytorch-cpu pip install  --no-cache-dir -U accelerate && \
    conda run -n pytorch-cpu pip install  --no-cache-dir "git+https://github.com/huggingface/optimum-intel.git" && \
    conda clean -y --all



RUN conda run -n pytorch-cpu conda install protobuf=4.24 -c conda-forge --override --force-reinstall -y

# PyTorch Installation
ARG IDP_VERSION
ARG DPNP_VERSION
ARG NUMPY_VERSION

ARG TORCH_GPU_VERSION
ARG ONECCL_GPU_VERSION
ARG IPEX_GPU_VERSION
ARG TORCHVISION_GPU_VERSION
ARG TORCHAUDIO_GPU_VERSION
ARG IDEX_VERSION
ARG DEEPSPEED_VERSION

# PyTorch GPU Env - conda packages
RUN conda create -yn pytorch-gpu -c intel/label/oneapi -c "${INTEL_CHANNEL}" -c conda-forge \
        dpnp="${DPNP_VERSION}" \
        dpcpp-cpp-rt="${IDP_VERSION}" \
        mkl-dpcpp="${IDP_VERSION}" \
        dpcpp_impl_linux-64="${IDP_VERSION}" \
        numpy="${NUMPY_VERSION}" \
        python="${PYTHON_VERSION}" \
        intel-openmp="${IDP_VERSION}" \
        python="${PYTHON_VERSION}" \
        pytorch="${TORCH_GPU_VERSION}" \
        oneccl_bind_pt="${ONECCL_GPU_VERSION}" \
        intel-extension-for-pytorch="${IPEX_GPU_VERSION}" \
        torchvision="${TORCHVISION_GPU_VERSION}" \
        torchaudio="${TORCHAUDIO_GPU_VERSION}" \
        tensorboardx \
        matplotlib-base \
        pandas \
        ipython \
        ipykernel \
        kernda  \
        'pillow>=10.2.0' \
        'aiohttp>=3.9.0' \
        'tornado>=6.3.3' \
        'jinja2>=3.1.3' \
        'idna>=3.7' \
        onnx \
        && \
    conda clean -y --all

# PyPI packages
RUN conda run -n pytorch-gpu pip install --no-deps --no-cache-dir --ignore-installed \
        ninja \
        python-dotenv \
        'tqdm>=4.66.2' \
        cloud-data-connector \
        dataset-librarian && \
    conda run -n pytorch-gpu pip install --no-cache-dir --ignore-installed \
        transformers \
        datasets \
        evaluate && \
    conda run -n pytorch-gpu pip install --no-cache-dir -U accelerate && \
    conda run -n pytorch-gpu pip install --no-cache-dir "git+https://github.com/huggingface/optimum-intel.git" && \
    conda clean -y --all



RUN conda run -n pytorch-gpu conda install protobuf=4.24 -c conda-forge --override --force-reinstall -y


# TensorFlow Installation
ARG IDP_VERSION
ARG DPNP_VERSION
ARG NUMPY_VERSION

ARG TF_VERSION
ARG ITEX_VERSION
ARG HOROVOD_VERSION
ARG IMPI_VERSION

ARG HOROVOD_WITH_TENSORFLOW=1
ARG HOROVOD_WITHOUT_MXNET=1
ARG HOROVOD_WITHOUT_GLOO=1
ARG HOROVOD_WITH_MPI=1


# Tensorflow Env - conda packages
RUN conda create -yn tensorflow-cpu -c "${INTEL_CHANNEL}" -c conda-forge \
        dpnp="${DPNP_VERSION}" \
        dpcpp-cpp-rt="${IDP_VERSION}" \
        mkl-dpcpp="${IDP_VERSION}" \
        numpy="${NUMPY_VERSION}" \
        python="${PYTHON_VERSION}" \
        intel-extension-for-tensorflow="${ITEX_VERSION}=*cpu*" \
        intel-optimization-for-horovod="${INTEL_HOROVOD}" \
        tensorflow="${TF_VERSION}" \
        impi-devel="${IMPI_VERSION}" \
        matplotlib-base \
        dataset_librarian \
        mpich=4.2.0=external_0 \
        ipython \
        ipykernel \
        kernda  \
        'pillow>=10.2.0' \
        'cryptography>=42.0.4' \
        'werkzeug>=2.2.3' \
        'aiohttp>=3.9.0' \
        'tornado>=6.3.3' \
        'pyjwt>=2.8.0' \
        'oauthlib>=3.2.2' \
        'idna>=3.7' \
        onnx \
        && \
    conda clean -y --all

# PyPI packages
RUN conda run -n tensorflow-cpu pip install --no-cache-dir --ignore-installed \
        py-cpuinfo \
        requests \
        cryptography
RUN conda run -n tensorflow-cpu pip install --no-deps --no-cache-dir --ignore-installed \
        tensorflow_hub \
        'tqdm>=4.66.2' \
        cloud-data-connector && \
    conda clean -y --all

# Tensorflow Env - conda packages
RUN conda create -yn tensorflow-gpu -c "${INTEL_CHANNEL}" -c conda-forge \
        dpnp="${DPNP_VERSION}" \
        dpcpp-cpp-rt="${IDP_VERSION}" \
        mkl-dpcpp="${IDP_VERSION}" \
        numpy="${NUMPY_VERSION}" \
        python="${PYTHON_VERSION}" \
        intel-extension-for-tensorflow="${ITEX_VERSION}=*xpu*" \
        intel-optimization-for-horovod="${INTEL_HOROVOD}" \
        tensorflow="${TF_VERSION}" \
        impi-devel="${IMPI_VERSION}" \
        matplotlib-base \
        dataset_librarian \
        mpich=4.2.0=external_0 \
        ipython \
        ipykernel \
        kernda  \
        'pillow>=10.2.0' \
        'cryptography>=42.0.4' \
        'werkzeug>=2.2.3' \
        'aiohttp>=3.9.0' \
        'tornado>=6.3.3' \
        'pyjwt>=2.8.0' \
        'oauthlib>=3.2.2' \
        'idna>=3.7' \
        onnx \
        && \
    conda clean -y --all

# PyPI packages
RUN conda run -n tensorflow-gpu pip install --no-cache-dir --ignore-installed \
        py-cpuinfo \
        requests \
        cryptography
RUN conda run -n tensorflow-gpu pip install --no-deps --no-cache-dir --ignore-installed \
        tensorflow_hub \
        'tqdm>=4.66.2' \
        cloud-data-connector  && \
    conda clean -y --all

FROM deep-learning-python as deep-learning-jupyter

ARG KERNEL_NAME_TF_CPU="Intel TensorFlow cpu"
ARG KERNEL_NAME_TF_GPU="Intel TensorFlow gpu"
ARG KERNEL_NAME_PT_CPU="Intel PyTorch cpu"
ARG KERNEL_NAME_PT_GPU="Intel PyTorch gpu"

EXPOSE 8888

RUN mkdir -p ~/jupyter/ && chmod -R a+rwx ~/jupyter/ && \
    mkdir ~/.local && chmod a+rwx ~/.local

RUN \
    "${CONDA_ROOT}/envs/pytorch-cpu/bin/python" -m ipykernel install --user --name pytorch-cpu --display-name "${KERNEL_NAME_PT_CPU}" && \
    "${CONDA_ROOT}/envs/pytorch-cpu/bin/kernda" -o -y "$HOME/.local/share/jupyter/kernels/$(echo pytorch-cpu | sed -e 's/\(.*\)/\L\1/')/kernel.json" && \
    "${CONDA_ROOT}/envs/pytorch-gpu/bin/python" -m ipykernel install --user --name pytorch-gpu --display-name "${KERNEL_NAME_PT_GPU}" && \
    "${CONDA_ROOT}/envs/pytorch-gpu/bin/kernda" -o -y "$HOME/.local/share/jupyter/kernels/$(echo pytorch-gpu | sed -e 's/\(.*\)/\L\1/')/kernel.json" && \
    "${CONDA_ROOT}/envs/tensorflow-cpu/bin/python" -m ipykernel install --user --name tensorflow-cpu --display-name "${KERNEL_NAME_TF_CPU}" && \
    "${CONDA_ROOT}/envs/tensorflow-cpu/bin/kernda" -o -y "$HOME/.local/share/jupyter/kernels/$(echo tensorflow-cpu | sed -e 's/\(.*\)/\L\1/')/kernel.json" && \
    "${CONDA_ROOT}/envs/tensorflow-gpu/bin/python" -m ipykernel install --user --name tensorflow-gpu --display-name "${KERNEL_NAME_TF_GPU}" && \
    "${CONDA_ROOT}/envs/tensorflow-gpu/bin/kernda" -o -y "$HOME/.local/share/jupyter/kernels/$(echo tensorflow-gpu | sed -e 's/\(.*\)/\L\1/')/kernel.json" && \
    python -m ipykernel.kernelspec --user

CMD ["bash", "-c", "jupyter lab --notebook-dir=~/jupyter --port 8888 --ip 0.0.0.0 --no-browser --allow-root"]

FROM deep-learning-jupyter as distributed-deep-learning

USER root

# Install OpenMPI
RUN apt-get update -y && apt-get install -y --no-install-recommends --fix-missing \
    libopenmpi-dev \
    openmpi-bin \
    openmpi-common

ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
ENV OMPI_MCA_tl_tcp_if_exclude="lo,docker0"

# Install OpenSSH
RUN apt-get install -y --no-install-recommends --fix-missing \
    openssh-client \
    openssh-server && \
    rm  /etc/ssh/ssh_host_*_key \
        /etc/ssh/ssh_host_*_key.pub && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/run/sshd

# https://github.com/openucx/ucx/issues/4742#issuecomment-584059909
ENV UCX_TLS=ud,sm,self

USER dev

RUN conda install -n pytorch-cpu -c intel/label/oneapi -c "${INTEL_CHANNEL}" -c conda-forge \
        deepspeed="${DEEPSPEED_VERSION}" \
        tensorboardx

RUN conda install -n pytorch-gpu -c intel/label/oneapi -c "${INTEL_CHANNEL}" -c conda-forge \
        deepspeed="${DEEPSPEED_VERSION}" \
        tensorboardx

COPY --chown=dev notebooks /home/dev/jupyter
COPY --chown=dev tests /home/dev/sample-tests
