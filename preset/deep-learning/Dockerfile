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


# This image provides a Python 3.9 environment you can use to run your Python
# applications.

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
    curl \
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
    xz-utils && \
    rm -rf /var/lib/apt/lists/*

# GPU Drivers setup
ARG DEVICE
ARG ICD_VER
ARG LEVEL_ZERO_GPU_VER
ARG LEVEL_ZERO_VER
ARG LEVEL_ZERO_DEV_VER
ARG DPCPP_VER
ARG MKL_VER

RUN wget -qO - https://repositories.intel.com/gpu/intel-graphics.key | \
      gpg --dearmor --output /usr/share/keyrings/intel-graphics.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/intel-graphics.gpg] https://repositories.intel.com/gpu/ubuntu jammy unified" | \
        tee /etc/apt/sources.list.d/intel-gpu-jammy.list &&\
    wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB \
        | gpg --dearmor | tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" \
        | tee /etc/apt/sources.list.d/oneAPI.list

RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
    intel-opencl-icd=${ICD_VER} \
    intel-level-zero-gpu=${LEVEL_ZERO_GPU_VER} \
    level-zero=${LEVEL_ZERO_VER} \
    level-zero-dev=${LEVEL_ZERO_DEV_VER} \
    intel-oneapi-runtime-dpcpp-cpp=${DPCPP_VER} \
    intel-oneapi-runtime-mkl=${MKL_VER} \
    libgl1-mesa-glx \
    libglib2.0-0  && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
FROM dgpu-base as deep-learning-python

# Setting up non-root directories
RUN useradd --uid 1000 -d /home/dev -s /bin/bash -m dev
USER dev
WORKDIR /home/dev

ENV CONDA_ROOT=/home/dev/conda

# Miniconda Python Installation
ARG MINICONDA_VERSION
ARG PYTHON_VERSION
ARG IDP_VERSION

RUN wget --no-check-certificate https://repo.anaconda.com/miniconda/Miniconda3-${MINICONDA_VERSION}.sh -O miniconda.sh && \        
    chmod +x miniconda.sh && \
    ./miniconda.sh -b -p ${CONDA_ROOT} && \
    rm ./miniconda.sh && \
    ln -s ${CONDA_ROOT} ${CONDA_ROOT}/../miniconda3 && \
    export PATH=${CONDA_ROOT}/bin/:${PATH} && \
    conda update -y conda && \
    conda config --add channels intel && \
    conda init --all && \
    python -m pip install --no-cache-dir jupyterlab jupyterhub notebook jupyter-server-proxy && \
    conda clean -y --all

ENV PATH ${CONDA_ROOT}/condabin:${CONDA_ROOT}/bin/:${PATH}
ENV LD_LIBRARY_PATH=/opt/intel/oneapi/lib:/opt/intel/oneapi/lib/intel64:${LD_LIBRARY_PATH}

# PyTorch Installation
ARG TORCH_CPU_VERSION
ARG ONECCL_CPU_VERSION
ARG IPEX_CPU_VERSION
ARG TORCHVISION_CPU_VERSION
ARG TORCH_GPU_VERSION
ARG ONECCL_GPU_VERSION
ARG IPEX_GPU_VERSION
ARG TORCHVISION_GPU_VERSION
ARG INTEL_CHANNEL
ARG NEURAL_COMPRESSOR_VERSION

# PyTorch CPU Env
RUN conda create -yn pytorch-cpu -c ${INTEL_CHANNEL} -c conda-forge \
        matplotlib-base \
        numba-dpex=0.21.4 \
        numpy=1.24.3 \
        ipp=2021.10 \
        intelpython=${IDP_VERSION} \
        python=${PYTHON_VERSION} \
        intel-openmp=2024.0 \
        pytorch=${TORCH_CPU_VERSION} \
        oneccl_bind_pt=${ONECCL_CPU_VERSION} \
        intel-extension-for-pytorch=${IPEX_CPU_VERSION} \
        torchvision=${TORCHVISION_CPU_VERSION} \
        onnx && \
    conda install -yn pytorch-cpu ipython ipykernel kernda -c conda-forge && \
    conda run -n pytorch-cpu python -m pip install --no-deps --no-cache-dir --ignore-installed \
        python-dotenv \
        tqdm \
        cloud-data-connector \
        dataset-librarian && \
    conda run -n pytorch-cpu python -m pip install --no-cache-dir \
        transformers \
        datasets \
        evaluate && \
    conda run -n pytorch-cpu python -m pip install -U accelerate && \
    conda run -n pytorch-cpu python -m pip install git+https://github.com/huggingface/optimum-intel.git && \
    conda clean -y --all && \
    echo "unset OCL_ICD_VENDORS" >> ${CONDA_ROOT}/envs/pytorch-cpu/etc/conda/activate.d/activate-opencl-rt.sh

# PyTorch GPU Env
RUN conda create -yn pytorch-gpu -c ${INTEL_CHANNEL} -c conda-forge \
        matplotlib-base \
        numba-dpex=0.21.4 \
        numpy=1.24.3 \
        ipp=2021.10 \
        intelpython=${IDP_VERSION} \
        python=${PYTHON_VERSION} \
        intel-openmp=2024.0 \
        pytorch=${TORCH_GPU_VERSION} \
        oneccl_bind_pt=${ONECCL_GPU_VERSION} \
        intel-extension-for-pytorch=${IPEX_GPU_VERSION} \
        torchvision=${TORCHVISION_GPU_VERSION} \
        onnx  && \
    conda install -yn pytorch-gpu ipython ipykernel kernda -c conda-forge  && \
    conda run -n pytorch-gpu python -m pip install --no-deps --no-cache-dir --ignore-installed \
        python-dotenv \
        tqdm \
        cloud-data-connector \
        dataset-librarian  && \
    conda run -n pytorch-gpu python -m pip install --no-cache-dir \
        transformers \
        datasets \
        evaluate  && \
    conda run -n pytorch-gpu python -m pip install -U accelerate && \
    conda run -n pytorch-gpu python -m pip install git+https://github.com/huggingface/optimum-intel.git && \
    conda clean -y --all && \
    echo "unset OCL_ICD_VENDORS" >> ${CONDA_ROOT}/envs/pytorch-gpu/etc/conda/activate.d/activate-opencl-rt.sh

# TensorFlow Installtion
ARG TF_PACKAGE
ARG TF_VERSION
ARG ITEX_VERSION
ARG INTEL_HOROVOD

# Install Horovod
ARG HOROVOD_VERSION
ARG HOROVOD_WITH_TENSORFLOW=1
ARG HOROVOD_WITHOUT_MXNET=1
ARG HOROVOD_WITHOUT_GLOO=1
ARG HOROVOD_WITH_MPI=1

RUN conda create -yn tensorflow -c ${INTEL_CHANNEL} -c conda-forge \
        matplotlib-base \
        numba-dpex=0.21.4 \
        numpy=1.24.3 \
        ipp=2021.10 \
        intelpython=${IDP_VERSION} \
        python=${PYTHON_VERSION} \
        intel-extension-for-tensorflow=${ITEX_VERSION} \
        intel-optimization-for-horovod=${INTEL_HOROVOD} \
        tensorflow=${TF_VERSION} \
        numpy=1.24.3 \
        impi-devel=2021.11 \
        dpnp \
        scipy \
        onnx
RUN conda install -yn tensorflow ipython ipykernel kernda -c conda-forge
RUN conda run -n tensorflow python -m pip install --no-cache-dir \
        tensorflow_hub \
        py-cpuinfo \
        requests \
        cryptography
RUN conda run -n tensorflow python -m pip install --no-deps --no-cache-dir --ignore-installed \
        python-dotenv \
        tqdm \
        cloud-data-connector \
        dataset-librarian && \
    conda clean -y --all && \
    echo "unset OCL_ICD_VENDORS" >> ${CONDA_ROOT}/envs/tensorflow/etc/conda/activate.d/activate-opencl-rt.sh

FROM deep-learning-python as deep-learning-jupyter

ARG KERNEL_NAME_PT="Intel PyTorch"
ARG KERNEL_NAME_TF="Intel TensorFlow"
EXPOSE 8888

RUN mkdir -p ~/jupyter/ && chmod -R a+rwx ~/jupyter/ && \
    mkdir ~/.local && chmod a+rwx ~/.local

RUN \
    ${CONDA_ROOT}/envs/pytorch-cpu/bin/python -m ipykernel install --user --name pytorch-cpu --display-name "${KERNEL_NAME_PT}" && \
    ${CONDA_ROOT}/envs/pytorch-cpu/bin/kernda -o -y ~/.local/share/jupyter/kernels/$(echo pytorch-cpu | sed -e 's/\(.*\)/\L\1/')/kernel.json && \
    ${CONDA_ROOT}/envs/pytorch-gpu/bin/python -m ipykernel install --user --name pytorch-gpu --display-name "${KERNEL_NAME_PT}" && \
    ${CONDA_ROOT}/envs/pytorch-gpu/bin/kernda -o -y ~/.local/share/jupyter/kernels/$(echo pytorch-gpu | sed -e 's/\(.*\)/\L\1/')/kernel.json && \
    ${CONDA_ROOT}/envs/tensorflow/bin/python -m ipykernel install --user --name tensorflow --display-name "${KERNEL_NAME_TF}" && \
    ${CONDA_ROOT}/envs/tensorflow/bin/kernda -o -y ~/.local/share/jupyter/kernels/$(echo tensorflow | sed -e 's/\(.*\)/\L\1/')/kernel.json && \
    python -m ipykernel.kernelspec --user

CMD ["bash", "-c", "jupyter notebook --notebook-dir=~/jupyter --port 8888 --ip 0.0.0.0 --no-browser --allow-root"]

FROM deep-learning-jupyter as distributed-deep-learning

USER root

# oneCCL installation
ARG CCL_VER="N/A"
RUN if [ ${CCL_VER} != "N/A" ]; then \
        apt-get update && \
        apt-get install -y --no-install-recommends --fix-missing \
        intel-oneapi-runtime-ccl=${CCL_VER} && \
        rm -rf /var/lib/apt/lists/*; \
    fi

# oneCCl specific flags
ENV CCL_ROOT="/opt/intel/oneapi/lib/intel64" 
ENV CCL_ZE_IPC_EXCHANGE=sockets
ENV LD_LIBRARY_PATH=/opt/intel/oneapi/lib/intel64/libfabric:${LD_LIBRARY_PATH}

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

RUN conda run -n pytorch-cpu python -m pip install --no-cache-dir py-cpuinfo && \
    conda run -n pytorch-cpu python -m pip install --no-cache-dir \
        deepspeed \
        intel-extension-for-deepspeed \
        tensorboardX
RUN conda run -n pytorch-gpu python -m pip install --no-cache-dir py-cpuinfo && \
    conda run -n pytorch-gpu python -m pip install --no-cache-dir \
        deepspeed \
        intel-extension-for-deepspeed \
        tensorboardX

COPY --chown=dev notebooks /home/dev/jupyter
COPY --chown=dev tests /home/dev/sample-tests
