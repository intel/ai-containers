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

##########################
# Setting up non-root directories
RUN useradd --uid 1000 -d /home/dev -s /bin/bash -m dev
USER dev
WORKDIR /home/dev

ENV CONDA_ROOT=/home/dev/conda
ARG MINIFORGE_VERSION
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

COPY requirements.txt .
RUN python -m pip install --no-cache-dir \
    --ignore-installed -r requirements.txt
RUN rm -rf requirements.txt

FROM deep-learning-base as deep-learning

##############################
# PyTorch Installation
ARG PYTHON_VERSION
ARG IDP_VERSION
ARG DPNP_VERSION
ARG NUMPY_VERSION
ARG TORCH_CPU_VERSION
ARG ONECCL_CPU_VERSION
ARG IPEX_CPU_VERSION
ARG TORCHVISION_CPU_VERSION
ARG TORCHAUDIO_CPU_VERSION
ARG DEEPSPEED_VERSION
ARG ONNXRUNTIME_VERSION
ARG NEURAL_COMPRESSOR_VERSION

RUN conda create -yn 'pytorch-cpu' \
    -c huggingface \
        "python=${PYTHON_VERSION}" \
        #####################
        'accelerate' \
        'mkl=2025.0.*' \
        "dpnp=${DPNP_VERSION}" \
        "intel-extension-for-pytorch=${IPEX_CPU_VERSION}" \
        "neural-compressor=${NEURAL_COMPRESSOR_VERSION}" \
        'ipykernel>=6.29.5' \
        'kernda>=0.3.0'  \
        'matplotlib-base>=3.10.1' \
        "oneccl_bind_pt=${ONECCL_CPU_VERSION}" \
        "pytorch=${TORCH_CPU_VERSION}" \
        'tensorboardx>=2.6.2.2' \
        "torchaudio=${TORCHAUDIO_CPU_VERSION}" \
        "torchvision=${TORCHVISION_CPU_VERSION}" \
        "onnxruntime=${ONNXRUNTIME_VERSION}" \
        "deepspeed=${DEEPSPEED_VERSION}" \
        && \
    conda clean -y --all

RUN conda clean --force-pkgs-dirs

COPY venv_requirements.txt .
RUN conda run -n 'pytorch-cpu' python -m pip install --no-cache-dir -r venv_requirements.txt && \
    conda clean -y --all
RUN rm -rf venv_requirements.txt

#######################################
# Adding jupyter capabilities
EXPOSE 8888

RUN mkdir -p ~/jupyter/ && chmod -R a+rwx ~/jupyter/ && \
    mkdir ~/.local && chmod a+rwx ~/.local

RUN CONDA_ENV="pytorch-cpu" && \
    KERNEL_NAME="PyTorch CPU" && \
    KERNEL_DIR="${CONDA_ROOT}/share/jupyter/kernels/$CONDA_ENV" && \
    conda run -n "$CONDA_ENV" python -m ipykernel install --prefix "$CONDA_ROOT" --name "$CONDA_ENV" --display-name "$KERNEL_NAME" && \
    conda run -n "$CONDA_ENV" kernda -o -y "$KERNEL_DIR/kernel.json" && \
    conda run -n base jupyter kernelspec list

CMD ["bash", "-c", "source activate pytorch-cpu && jupyter lab --notebook-dir=~/jupyter --port 8888 --ip 0.0.0.0 --no-browser --allow-root"]

COPY --chown=dev notebooks /home/dev/jupyter
COPY --chown=dev tests /home/dev/sample-tests

ENV BASH_ENV ~/.bash_profile
RUN echo "conda activate pytorch-cpu" >> ~/.bashrc
