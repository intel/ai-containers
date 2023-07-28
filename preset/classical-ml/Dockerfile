ARG BASE_IMAGE="ubuntu"
ARG BASE_TAG="22.04"

FROM ${BASE_IMAGE}:${BASE_TAG} as classical-ml-base

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
    xz-utils

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

ARG SCIKIT_VERSION
ARG XGBOOST_VERSION
ARG MODIN_VERSION

RUN mkdir -p /licensing && \
	wget -O - https://github.com/intel/scikit-learn-intelex/archive/refs/tags/${SCIKIT_VERSION}.tar.gz | \
	tar -xz -C /licensing --strip=2 "scikit-learn-intelex-${SCIKIT_VERSION}/doc/third-party-programs-sklearnex.txt" \
	"scikit-learn-intelex-${SCIKIT_VERSION}/doc/daal4py/third-party-programs.txt"

RUN curl https://raw.githubusercontent.com/intel/scikit-learn-intelex/${SCIKIT_VERSION}/LICENSE -o /licensing/SCIKIT_LICENSE

RUN conda create -yn classical-ml intelpython3_core==${IDP_VERSION} python=${PYTHON_VERSION} && \
    conda install -yn classical-ml ipython ipykernel kernda -c conda-forge && \
    conda install -n classical-ml -y -c intel \
    matplotlib \
    daal4py \
    scikit-learn-intelex${SCIKIT_VERSION:+==${SCIKIT_VERSION}} \
    threadpoolctl

RUN conda install -n classical-ml -y -c intel xgboost${XGBOOST_VERSION:+==${XGBOOST_VERSION}}
RUN conda run -n classical-ml python -m pip install --ignore-installed modin[ray]==${MODIN_VERSION} dataset-librarian

ENV LD_LIBRARY_PATH /workspace/libssl/lib/:${LD_LIBRARY_PATH}
ENV BASH_ENV /root/.bash_profile
RUN echo "conda activate classical-ml" >> ~/.bashrc

ENV PYTHONSTARTUP=${HOME}/.patch_sklearn.py
COPY base/.patch_sklearn.py ${HOME}/.patch_sklearn.py

FROM classical-ml-base as jupyter

ENV PORT=8888
EXPOSE $PORT


RUN mkdir -p /jupyter/ && chmod -R a+rwx /jupyter/ && \
    mkdir /.local && chmod a+rwx /.local

WORKDIR /jupyter

RUN conda run -n classical-ml python -m pip install --no-cache-dir jupyterlab jupyterhub notebook jupyter-server-proxy && \
    ~/conda/envs/classical-ml/bin/python -m ipykernel install --name classical-ml --display-name "Classical ML" && \
    ~/conda/envs/classical-ml/bin/kernda -o -y /usr/local/share/jupyter/kernels/$(echo classical-ml | sed -e 's/\(.*\)/\L\1/')/kernel.json && \
    ~/conda/envs/classical-ml/bin/python -m ipykernel.kernelspec && \
    conda clean -y --all

CMD ["bash", "-c", "source activate classical-ml && jupyter notebook --notebook-dir=/jupyter --port $PORT --ip 0.0.0.0 --no-browser --allow-root"]
