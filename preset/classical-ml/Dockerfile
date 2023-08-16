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
    git \
    gzip \
    make \
    patch \
    rsync \
    unzip \
    wget \
    xz-utils

#Remove apt utilities from container
RUN rm -rf /usr/bin/apt*

FROM classical-ml-base as classical-ml-python

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

ARG SCIKIT_VERSION
ARG XGBOOST_VERSION
ARG MODIN_VERSION

RUN mkdir -p ~/licensing && \
	wget -O - https://github.com/intel/scikit-learn-intelex/archive/refs/tags/${SCIKIT_VERSION}.tar.gz | \
	tar -xz -C ~/licensing --strip=2 "scikit-learn-intelex-${SCIKIT_VERSION}/doc/third-party-programs-sklearnex.txt" \
	"scikit-learn-intelex-${SCIKIT_VERSION}/doc/daal4py/third-party-programs.txt" && \
    curl https://raw.githubusercontent.com/intel/scikit-learn-intelex/${SCIKIT_VERSION}/LICENSE -o ~/licensing/SCIKIT_LICENSE

RUN conda create -yn classical-ml intelpython3_core==${IDP_VERSION} python=${PYTHON_VERSION} && \
    conda install -yn classical-ml ipython ipykernel kernda -c conda-forge && \
    conda install -n classical-ml -y -c intel \
    matplotlib \
    daal4py \
    scikit-learn-intelex${SCIKIT_VERSION:+==${SCIKIT_VERSION}} \
    threadpoolctl && \
    conda clean -y --all

RUN conda install -n classical-ml -y -c intel xgboost${XGBOOST_VERSION:+==${XGBOOST_VERSION}} &&\
    conda clean -y --all
RUN conda run -n classical-ml python -m pip install --ignore-installed --no-cache-dir \
        modin[ray]==${MODIN_VERSION} \
        dataset-librarian \
        cloud-data-connector && \
    conda run -n classical-ml python -m pip install --no-cache-dir \
        scipy==1.11.1 \
        certifi=='2023.07.22'

ENV PYTHONSTARTUP=~/.patch_sklearn.py
COPY base/.patch_sklearn.py ~/.patch_sklearn.py

ENV PYTHONSTARTUP=/home/${USERNAME}/.patch_sklearn.py
COPY base/.patch_sklearn.py /home/${USERNAME}/.patch_sklearn.py

FROM classical-ml-python as classical-ml-jupyter

ENV PORT=8888
EXPOSE $PORT

RUN mkdir -p ~/jupyter/ && chmod -R a+rwx ~/jupyter/ && \
    mkdir ~/.local && chmod a+rwx ~/.local

WORKDIR /home/${USERNAME}/jupyter

RUN conda run -n classical-ml python -m pip install --no-cache-dir jupyterlab jupyterhub notebook jupyter-server-proxy && \
    ${CONDA_ROOT}/envs/classical-ml/bin/python -m ipykernel install --user --name classical-ml --display-name "Classical ML" && \
    ${CONDA_ROOT}/envs/classical-ml/bin/kernda -o -y ~/.local/share/jupyter/kernels/$(echo classical-ml | sed -e 's/\(.*\)/\L\1/')/kernel.json && \
    ${CONDA_ROOT}/envs/classical-ml/bin/python -m ipykernel.kernelspec --user && \
    conda clean -y --all

CMD ["bash", "-c", "source activate classical-ml && jupyter notebook --notebook-dir=~/jupyter --port $PORT --ip 0.0.0.0 --no-browser --allow-root"]

ENV BASH_ENV ~/.bash_profile
RUN echo "conda activate classical-ml" >> ~/.bashrc
