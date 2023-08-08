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
    gzip \
    make \
    patch \
    rsync \
    unzip \
    wget \
    xz-utils && \
    rm -rf /var/lib/apt/lists/*

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
    conda clean -y --all

ENV PATH /root/conda/condabin:~/conda/bin/:${PATH}

RUN conda create -yn data-analytics intelpython3_core=${IDP_VERSION} python=${PYTHON_VERSION} && \
    conda install -yn data-analytics ipython ipykernel kernda -c conda-forge && \
    conda run -n data-analytics python -m pip install --ignore-installed --no-cache-dir \
        modin[ray] \
        dataset-librarian \
        cloud-data-connector && \
    conda run -n data-analytics python -m pip install --no-cache-dir \
        scipy==1.11.1 && \
    conda clean -y --all

ENV BASH_ENV /root/.bash_profile
RUN echo "conda activate data-analytics" >> ~/.bashrc

FROM data-analytics-base as jupyter

ENV PORT=8888
EXPOSE $PORT


RUN mkdir -p /jupyter/ && chmod -R a+rwx /jupyter/ && \
    mkdir /.local && chmod a+rwx /.local

WORKDIR /jupyter

RUN conda run -n data-analytics python -m pip install --no-cache-dir jupyterlab jupyterhub notebook jupyter-server-proxy && \
    ~/conda/envs/data-analytics/bin/python -m ipykernel install --name data-analytics --display-name "Data Analytics" && \
    ~/conda/envs/data-analytics/bin/kernda -o -y /usr/local/share/jupyter/kernels/$(echo data-analytics | sed -e 's/\(.*\)/\L\1/')/kernel.json && \
    ~/conda/envs/data-analytics/bin/python -m ipykernel.kernelspec && \
    conda clean -y --all

CMD ["bash", "-c", "source activate data-analytics && jupyter notebook --notebook-dir=/jupyter --port $PORT --ip 0.0.0.0 --no-browser --allow-root"]

