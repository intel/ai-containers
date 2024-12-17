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


ARG BASE_IMAGE="ubuntu"
ARG BASE_TAG="22.04"

FROM ${BASE_IMAGE}:${BASE_TAG} AS conda-base

ENV DEBIAN_FRONTEND=noninteractive

ENV LANG=C.UTF-8

SHELL ["/bin/bash", "-c"]

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends --fix-missing \
        bzip2 \
        ca-certificates \
        gcc \
        git \
        gzip \
        make \
        rsync \
        unzip \
        wget \
        xz-utils && \
    rm -rf /var/lib/apt/lists/*

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
        'libarchive>=3.7.7' \
    && \
    jupyter labextension disable "@jupyterlab/apputils-extension:announcements" \
    && \
    conda clean -y --all \
    && \
    conda config --add channels ${INTEL_CHANNEL}

ENV PATH ${CONDA_ROOT}/condabin:${CONDA_ROOT}/bin/:${PATH}
RUN conda config --set pip_interop_enabled True

COPY requirements.txt .
RUN python -m pip install --no-cache-dir \
    --ignore-installed -r requirements.txt

FROM conda-base as deep-learning

ARG IDP_VERSION
ARG DPNP_VERSION
ARG MODIN_VERSION
ARG NUMPY_VERSION
ARG MKL_VERSION

# JAX  Installation
ARG PYTHON_VERSION
ARG IDP_VERSION
ARG NUMPY_VERSION
ARG JAX_VERSION


RUN conda create -yn 'jax-cpu' \
        "python=${PYTHON_VERSION}" \
        "jax=${JAX_VERSION}" \
        "numpy=${NUMPY_VERSION}" \
        "mkl=${MKL_VERSION}" \
        'ipykernel>=6.29.5' \
        'kernda>=0.3.0' \
        'zipp>=3.19.1' \
        && \
    conda clean -y --all

EXPOSE 8888

RUN mkdir -p ~/jupyter/ && chmod -R a+rwx ~/jupyter/ && \
    mkdir ~/.local && chmod a+rwx ~/.local

WORKDIR /home/dev
COPY --chown=dev tests /home/dev/sample-tests

RUN CONDA_ENV="jax-cpu" && \
    KERNEL_NAME="JAX CPU" && \
    KERNEL_DIR="${CONDA_ROOT}/share/jupyter/kernels/$CONDA_ENV" && \
    conda run -n "$CONDA_ENV" python -m ipykernel install --prefix "$CONDA_ROOT" --name "$CONDA_ENV" --display-name "$KERNEL_NAME" && \
    conda run -n "$CONDA_ENV" kernda -o -y "$KERNEL_DIR/kernel.json" && \
    conda run -n base jupyter kernelspec list

CMD ["bash", "-c", "source activate jax-cpu && jupyter lab --notebook-dir=~/jupyter --port 8888 --ip 0.0.0.0 --no-browser --allow-root"]

ENV BASH_ENV ~/.bash_profile
RUN echo "conda activate jax-cpu" >> ~/.bashrc
