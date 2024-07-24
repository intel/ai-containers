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

FROM ${BASE_IMAGE}:${BASE_TAG} as data-analytics

ENV DEBIAN_FRONTEND=noninteractive

# See http://bugs.python.org/issue19846

ENV LANG=C.UTF-8

SHELL ["/bin/bash", "-c"]

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends --fix-missing \
    bzip2 \
    ca-certificates \
    diffutils \
    gcc \
    git \
    gzip \
    make \
    patch \
    rsync \
    unzip \
    wget \
    xz-utils && \
    rm -rf /var/lib/apt/lists/*

# Setting up non-root directories
RUN useradd --uid 1000 -d /home/dev -s /bin/bash -m dev
# Set a password for the user (Optional)
RUN echo 'dev:password' | chpasswd
USER dev
WORKDIR /home/dev

ENV CONDA_ROOT=/home/dev/conda
ARG MINIFORGE_VERSION
ARG PYTHON_VERSION
ARG IDP_VERSION
ARG INTEL_CHANNEL

RUN wget --progress=dot:giga --no-check-certificate "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-${MINIFORGE_VERSION}.sh" -O miniforge.sh && \
    chmod +x miniforge.sh && \
    ./miniforge.sh -b -p "${CONDA_ROOT}" && \
    rm ./miniforge.sh && \
    ln -s "${CONDA_ROOT}" "${CONDA_ROOT}/../miniforge3" && \
    export PATH="${CONDA_ROOT}/bin/:${PATH}" && \
    conda init --all && \
    conda install -y \
        'colorama==0.4.6' \
        'conda==24.5.0' \
        'jupyterhub==5.0.0' \
        'jupyter-server-proxy==4.3.0' \
        'mamba==1.5.8' \
        'networkx==3.3' \
        'notebook==7.2.1' \
        'python==3.10.14' \
    && \
    jupyter labextension disable "@jupyterlab/apputils-extension:announcements" \
    && \
    conda clean -y --all \
    && \
    conda config --add channels ${INTEL_CHANNEL}

ENV PATH ${CONDA_ROOT}/condabin:${CONDA_ROOT}/bin/:${PATH}
RUN conda config --set pip_interop_enabled True

ARG IDP_VERSION
ARG DPNP_VERSION
ARG MODIN_VERSION
ARG NUMPY_VERSION

# data-analytics Env - conda packages
RUN conda create -yn data-analytics \
        "python=${PYTHON_VERSION}" \
        "dpnp=${DPNP_VERSION}" \
        'ipykernel==6.29.5' \
        'kernda==0.3.0' \
        'matplotlib-base==3.8.4' \
        "modin-ray=${MODIN_VERSION}" \
        'python-dotenv==1.0.1' \
        'tqdm==4.66.4' \
        && \
    conda clean -y --all

RUN conda run -n data-analytics python -m pip install --no-deps --no-cache-dir \
    'dataset-librarian==1.0.4'

EXPOSE 8888

RUN mkdir -p ~/jupyter/ && chmod -R a+rwx ~/jupyter/ && \
    mkdir ~/.local && chmod a+rwx ~/.local

COPY --chown=dev notebooks /home/dev/jupyter
COPY --chown=dev tests /home/dev/sample-tests

RUN KERNEL_DIR="${CONDA_ROOT}/envs/data-analytics/share/jupyter/kernels/data-analytics" && \
    conda run -n data-analytics python -m ipykernel install --prefix "${CONDA_ROOT}/envs/data-analytics" --name data-analytics --display-name "Data Analytics" && \
    conda run -n data-analytics kernda -o -y "$KERNEL_DIR/kernel.json" && \
    conda run -n data-analytics jupyter kernelspec list

CMD ["bash", "-c", "source activate data-analytics && jupyter lab --notebook-dir=~/jupyter --port 8888 --ip 0.0.0.0 --no-browser --allow-root"]

ENV BASH_ENV ~/.bash_profile
RUN echo "conda activate data-analytics" >> ~/.bashrc
