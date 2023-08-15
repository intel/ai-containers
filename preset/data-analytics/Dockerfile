ARG BASE_IMAGE="ubuntu"
ARG BASE_TAG="22.04"

FROM ${BASE_IMAGE}:${BASE_TAG} as data-analytics-base

ENV DEBIAN_FRONTEND=noninteractive

# See http://bugs.python.org/issue19846

ENV LANG=C.UTF-8

SHELL ["/bin/bash", "-c"]

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends --fix-missing \
    bzip2 \
    ca-certificates \
    curl \
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

#Remove apt utilities from container
RUN rm -rf /usr/bin/apt*

FROM data-analytics-base as data-analytics-python

#Setting up non-root directories
ARG USERNAME
RUN useradd --uid 1000 -d /home/${USERNAME} -s /bin/bash -m ${USERNAME}
USER $USERNAME
WORKDIR /home/${USERNAME}

ENV CONDA_ROOT=/home/${USERNAME}/conda

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
    conda clean -y --all

ENV PATH ${CONDA_ROOT}/condabin:${CONDA_ROOT}/bin/:${PATH}

RUN conda create -yn data-analytics intelpython3_core=${IDP_VERSION} python=${PYTHON_VERSION} && \
    conda install -yn data-analytics ipython ipykernel kernda -c conda-forge && \
    conda run -n data-analytics python -m pip install --ignore-installed --no-cache-dir \
        modin[ray] \
        dataset-librarian \
        cloud-data-connector && \
    conda run -n data-analytics python -m pip install --no-cache-dir \
        scipy==1.11.1 && \
    conda clean -y --all

FROM data-analytics-python as data-analytics-jupyter

ENV PORT=8888
EXPOSE $PORT


RUN mkdir -p ~/jupyter/ && chmod -R a+rwx ~/jupyter/ && \
    mkdir ~/.local && chmod a+rwx ~/.local

WORKDIR /home/${USERNAME}/jupyter

RUN conda run -n data-analytics python -m pip install --no-cache-dir jupyterlab jupyterhub notebook jupyter-server-proxy && \
    ${CONDA_ROOT}/envs/data-analytics/bin/python -m ipykernel install --user --name data-analytics --display-name "Data Analytics" && \
    ${CONDA_ROOT}/envs/data-analytics/bin/kernda -o -y ~/.local/share/jupyter/kernels/$(echo data-analytics | sed -e 's/\(.*\)/\L\1/')/kernel.json && \
    ${CONDA_ROOT}/envs/data-analytics/bin/python -m ipykernel.kernelspec --user && \
    conda clean -y --all

CMD ["bash", "-c", "source activate data-analytics && jupyter notebook --notebook-dir=~/jupyter --port $PORT --ip 0.0.0.0 --no-browser --allow-root"]

ENV BASH_ENV ~/.bash_profile
RUN echo "conda activate data-analytics" >> ~/.bashrc
