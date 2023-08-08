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
    patch \
    rsync \
    unzip \
    wget \
    xz-utils && \
    rm -rf /var/lib/apt/lists/*

#GPU Drivers setup

ARG DEVICE
ARG ICD_VER
ARG LEVEL_ZERO_GPU_VER
ARG LEVEL_ZERO_VER
ARG LEVEL_ZERO_DEV_VER
ARG DPCPP_VER
ARG MKL_VER

RUN wget -qO - https://repositories.intel.com/graphics/intel-graphics.key | \
    gpg --dearmor --output /usr/share/keyrings/intel-graphics.gpg && \
    printf 'deb [arch=amd64 signed-by=/usr/share/keyrings/intel-graphics.gpg] https://repositories.intel.com/graphics/ubuntu jammy %s\n' "$DEVICE" | \
    tee  /etc/apt/sources.list.d/intel.gpu.jammy.list && \
    wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB \
   | gpg --dearmor | tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null && \
   echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" \
   | tee /etc/apt/sources.list.d/oneAPI.list && \
    apt-get update && \
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

FROM dgpu-base as deep-learning-base

#Miniconda Python Installation
ARG MINICONDA_VERSION
ARG PYTHON_VERSION
ARG IDP_VERSION

RUN wget --no-check-certificate https://repo.anaconda.com/miniconda/Miniconda3-${MINICONDA_VERSION}.sh -O miniconda.sh && \        
    chmod +x miniconda.sh && \
    ./miniconda.sh -b -p ~/conda && \
    rm ./miniconda.sh && \
    ln -s ~/conda ~/miniconda3 && \
    export PATH=~/conda/bin/:${PATH} && \
    conda update -y conda && \
    conda config --add channels intel && \
    conda init --all && \
    python -m pip install --no-cache-dir jupyterlab jupyterhub notebook jupyter-server-proxy && \
    conda clean -y --all

ENV PATH /root/conda/condabin:~/conda/bin/:${PATH}
ENV LD_LIBRARY_PATH=/opt/intel/oneapi/lib:/opt/intel/oneapi/lib/intel64:${LD_LIBRARY_PATH}

#PyTorch Installation
ARG TORCH_VERSION
ARG TORCHVISION_VERSION
ARG IPEX_VERSION
ARG TORCH_WHL_URL
ARG IPEX_WHL_URL
ARG TORCHVISION_WHL_URL

RUN \
    conda create -yn torch intelpython3_core=${IDP_VERSION} python=${PYTHON_VERSION} && \
    conda install -yn torch ipython ipykernel kernda -c conda-forge && \
    conda install -yn torch matplotlib -c intel && \
    conda run -n torch python -m pip install --no-cache-dir -f ${TORCH_WHL_URL} \
        torch==${TORCH_VERSION} \
        intel_extension_for_pytorch==${IPEX_VERSION} \
        torchvision==${TORCHVISION_VERSION} -f ${TORCHVISION_WHL_URL} && \
    conda run -n torch python -m pip install --no-cache-dir --ignore-installed \
        cloud-data-connector \
        dataset-librarian && \
    conda run -n torch python -m pip install --no-cache-dir \
        scipy==1.11.1 \
        certifi=='2023.07.22' && \
    conda clean -y --all

RUN echo "unset OCL_ICD_VENDORS" >> ~/conda/envs/torch/etc/conda/activate.d/activate-opencl-rt.sh

#Tensorflow Installtion
ARG TF_PACKAGE
ARG TF_PACKAGE_VERSION
ARG ITEX_VERSION

RUN conda create -yn tensorflow intelpython3_core python=${PYTHON_VERSION} && \
    conda install -yn tensorflow ipython ipykernel kernda -c conda-forge && \
    conda run -n tensorflow python -m pip install --no-cache-dir ${TF_PACKAGE}${TF_PACKAGE_VERSION:+==${TF_PACKAGE_VERSION}} \
        intel-extension-for-tensorflow[xpu]==${ITEX_VERSION} \
        requests==2.31.0 \
        cryptography==41.0.2 && \
    conda run -n tensorflow python -m pip install --no-cache-dir --ignore-installed \
        cloud-data-connector \
        dataset-librarian && \
    conda run -n tensorflow python -m pip install --no-cache-dir \
        scipy==1.11.1 \
        certifi=='2023.07.22' && \
    conda clean -y --all

RUN echo "unset OCL_ICD_VENDORS" >> ~/conda/envs/tensorflow/etc/conda/activate.d/activate-opencl-rt.sh

FROM deep-learning-base as deep-learning-jupyter

ARG KERNEL_NAME_PT="Intel PyTorch"
ARG KERNEL_NAME_TF="Intel TensorFlow"
ENV PORT=8888
EXPOSE $PORT

RUN \
    ~/conda/envs/torch/bin/python -m ipykernel install --name torch --display-name "${KERNEL_NAME_PT}" && \
    ~/conda/envs/torch/bin/kernda -o -y /usr/local/share/jupyter/kernels/$(echo torch | sed -e 's/\(.*\)/\L\1/')/kernel.json && \
    ~/conda/envs/tensorflow/bin/python -m ipykernel install --name tensorflow --display-name "${KERNEL_NAME_TF}" && \
    ~/conda/envs/tensorflow/bin/kernda -o -y /usr/local/share/jupyter/kernels/$(echo tensorflow | sed -e 's/\(.*\)/\L\1/')/kernel.json

RUN mkdir -p /jupyter/ && chmod -R a+rwx /jupyter/ && \
    mkdir /.local && chmod a+rwx /.local

WORKDIR /jupyter

RUN python -m ipykernel.kernelspec

CMD ["bash", "-c", "jupyter notebook --notebook-dir=/jupyter --port $PORT --ip 0.0.0.0 --no-browser --allow-root"]

FROM deep-learning-jupyter as distributed-deep-learning

#oneccl installation
ARG CCL_VER="N/A"
RUN if [ ${CCL_VER} != "N/A" ]; then \
        apt-get update && \
        apt-get install -y --no-install-recommends --fix-missing \
        intel-oneapi-runtime-ccl=${CCL_VER} && \
        rm -rf /var/lib/apt/lists/*; \
    fi

ENV LD_LIBRARY_PATH=/opt/intel/oneapi/lib/intel64/libfabric:${LD_LIBRARY_PATH}
#Needed by OneCCl operations
ENV CCL_ROOT="/opt/intel/oneapi/lib/intel64" 
ENV CCL_ZE_IPC_EXCHANGE=sockets
ARG ONECCL_BIND_PT_WHL_URL="N/A"
ARG ONECCL_BIND_PT_VERSION="N/A"

RUN conda run -n torch python -m pip install --no-cache-dir \
        oneccl_bind_pt==${ONECCL_BIND_PT_VERSION} -f ${ONECCL_BIND_PT_WHL_URL} \
        py-cpuinfo \
        intel-extension-for-deepspeed && \
    conda run -n torch python -m pip install --no-cache-dir deepspeed

#Install OpenMPI
RUN apt-get update -y && apt-get install -y --no-install-recommends --fix-missing \
    libopenmpi-dev \
    openmpi-bin \
    openmpi-common \
    openssh-client \
    openssh-server && \
    rm -rf /var/lib/apt/lists/*

ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

ENV OMPI_MCA_tl_tcp_if_exclude="lo,docker0"

# Install OpenSSH for MPI to communicate between containers
RUN mkdir -p /var/run/sshd

# Install Horovod
ARG HOROVOD_VERSION
ARG HOROVOD_WITH_TENSORFLOW=1
ARG HOROVOD_WITHOUT_MXNET=1
ARG HOROVOD_WITHOUT_GLOO=1
ARG HOROVOD_WITH_MPI=1

RUN conda run -n tensorflow python -m pip install --no-cache-dir intel-optimization-for-horovod${HOROVOD_VERSION+==${HOROVOD_VERSION}} && \
    conda clean -y --all

FROM deep-learning-jupyter as inc-base

ENV SIGOPT_PROJECT=.

ARG INC_VERSION: ${INC_VERSION:-2.2.1}

RUN conda run -n torch python -m pip install --no-cache-dir \
        neural-compressor${INC_VERSION:+==${INC_VERSION}} \
        numpy==1.23.5 && \
    conda clean -y --all

RUN conda run -n tensorflow python -m pip install --no-cache-dir \
        neural-compressor${INC_VERSION:+==${INC_VERSION}} \
        numpy==1.23.5 \
        tf2onnx && \
    conda clean -y --all
