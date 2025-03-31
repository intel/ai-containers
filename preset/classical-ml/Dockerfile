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

FROM ${BASE_IMAGE}:${BASE_TAG} as classical-ml

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

# Setting up non-root directories
RUN useradd --uid 1000 -d /home/dev -s /bin/bash -m dev
USER dev
WORKDIR /home/dev

ENV CONDA_ROOT=/home/dev/conda
ARG MINIFORGE_VERSION
ARG INTEL_CHANNEL

RUN wget --progress=dot:giga --no-check-certificate https://github.com/conda-forge/miniforge/releases/latest/download/${MINIFORGE_VERSION}.sh -O miniforge.sh && \
    chmod +x miniforge.sh && \
    ./miniforge.sh -b -p "${CONDA_ROOT}" && \
    rm ./miniforge.sh && \
    ln -s "${CONDA_ROOT}" "${CONDA_ROOT}/../miniforge" && \
    export PATH="${CONDA_ROOT}/bin/:${PATH}" && \
    conda init --all && \
    conda update -y conda && \
    conda install -y \
        'jupyterlab>=4.2.6' \
        'notebook>=7.1.3' \
        'nb_conda_kernels>=2.5.1' \
        'libexpat>=2.7.0' \
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

ARG PYTHON_VERSION
ARG IDP_VERSION
ARG DAAL4PY_VERSION
ARG DPNP_VERSION
ARG XGBOOST_VERSION
ARG MODIN_VERSION
ARG NUMPY_VERSION
ARG SKLEARNEX_VERSION
ARG MKL_VERSION

RUN conda create -yn classical-ml \
        "python=${PYTHON_VERSION}" \
        "mkl=${MKL_VERSION}" \
        "dpnp=${DPNP_VERSION}" \
        'ipykernel>=6.29.5' \
        'kernda>=0.3.0' \
        'matplotlib-base>=3.10.1' \
        "modin-ray=${MODIN_VERSION}" \
        "ray-core>2.9" \
        "scikit-learn-intelex=${SKLEARNEX_VERSION}" \
        "xgboost=${XGBOOST_VERSION}" \
        "scikit-learn"=1.5.2 \
        'libexpat>=2.7.0' \
        && \
    conda clean -y --all

ENV PYTHONSTARTUP=~/.patch_sklearn.py
COPY base/.patch_sklearn.py ~/.patch_sklearn.py

ENV PYTHONSTARTUP=/home/dev/.patch_sklearn.py
COPY base/.patch_sklearn.py /home/dev/.patch_sklearn.py

EXPOSE 8888

RUN mkdir -p ~/jupyter/ && chmod -R a+rwx ~/jupyter/ && \
    mkdir ~/.local && chmod a+rwx ~/.local

WORKDIR /home/dev
COPY --chown=dev notebooks /home/dev/jupyter
COPY --chown=dev tests /home/dev/sample-tests

RUN KERNEL_DIR="${CONDA_ROOT}/share/jupyter/kernels/classical-ml" && \
    conda run -n classical-ml python -m ipykernel install --prefix "$CONDA_ROOT" --name classical-ml --display-name "Classical ML" && \
    conda run -n classical-ml kernda -o -y "$KERNEL_DIR/kernel.json" && \
    conda run -n base jupyter kernelspec list

CMD ["bash", "-c", "source activate classical-ml && jupyter lab --notebook-dir=~/jupyter --port 8888 --ip 0.0.0.0 --no-browser --allow-root"]

ENV BASH_ENV ~/.bash_profile
RUN echo "conda activate classical-ml" >> ~/.bashrc
