# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
#
#
# This file was assembled from multiple pieces, whose use is documented
# throughout. Please refer to the TensorFlow dockerfiles documentation
# for more information.

ARG BASE_IMAGE_NAME=ubuntu
ARG BASE_IMAGE_TAG=22.04
ARG PACKAGE_OPTION=pip
FROM ${BASE_IMAGE_NAME}:${BASE_IMAGE_TAG} AS base

# See http://bugs.python.org/issue19846
ENV LANG C.UTF-8
ARG PYTHON_VERSION

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install -y --no-install-recommends --fix-missing \
    ca-certificates \
    curl \
    wget

ARG SCIKIT_VERSION
ARG XGBOOST_VERSION

RUN mkdir -p /licensing && \
	wget -O - https://github.com/intel/scikit-learn-intelex/archive/refs/tags/${SCIKIT_VERSION}.tar.gz | \
	tar -xz -C /licensing --strip=2 "scikit-learn-intelex-${SCIKIT_VERSION}/doc/third-party-programs-sklearnex.txt" \
	"scikit-learn-intelex-${SCIKIT_VERSION}/doc/daal4py/third-party-programs.txt"

RUN curl https://raw.githubusercontent.com/intel/scikit-learn-intelex/${SCIKIT_VERSION}/LICENSE -o /licensing/SCIKIT_LICENSE

FROM base AS ml-base-pip

RUN apt-get install -y --no-install-recommends --fix-missing \
    python${PYTHON_VERSION} \
    python${PYTHON_VERSION}-distutils \
    python3-pip

RUN ln -sf $(which python${PYTHON_VERSION}) /usr/local/bin/python && \
    ln -sf $(which python${PYTHON_VERSION}) /usr/local/bin/python3 && \
    ln -sf $(which python${PYTHON_VERSION}) /usr/bin/python

RUN python -m pip --no-cache-dir install --upgrade \
    pip \
    setuptools

RUN python -m pip install --no-cache-dir \
    daal4py \
    scikit-learn-intelex${SCIKIT_VERSION:+==${SCIKIT_VERSION}} \
    threadpoolctl \
    xgboost${XGBOOST_VERSION:+==${XGBOOST_VERSION}}

COPY base/.patch_sklearn.py ${HOME}/.patch_sklearn.py

FROM idp-core AS ml-base-idp

ENV BASH_ENV /root/.bash_profile

RUN echo "conda activate idp" >> ~/.bashrc

RUN ln -sf /root/conda/envs/idp/bin/python /usr/local/bin/python && \
    ln -sf /root/conda/envs/idp/bin/python /usr/local/bin/python3 && \
    ln -sf /root/conda/envs/idp/bin/python /usr/bin/python

RUN conda install -n idp -y -c intel \
    daal4py \
    scikit-learn-intelex${SCIKIT_VERSION:+==${SCIKIT_VERSION}}

RUN python -m pip install --no-cache-dir \
    # https://github.com/intel/scikit-learn-intelex/blob/master/requirements-test.txt
    numpy==1.23.0 \ 
    threadpoolctl \
    xgboost${XGBOOST_VERSION:+==${XGBOOST_VERSION}} && \
    apt-get clean && conda clean -y --all

ENV PYTHONSTARTUP=${HOME}/.patch_sklearn.py
COPY base/.patch_sklearn.py ${HOME}/.patch_sklearn.py

FROM ml-base-${PACKAGE_OPTION} AS jupyter

RUN python -m pip install --no-cache-dir jupyter matplotlib jupyter_http_over_ws ipykernel nbformat
RUN python -m jupyter serverextension enable --py jupyter_http_over_ws

RUN mkdir -p /jupyter/ && chmod -R a+rwx /jupyter/
RUN mkdir /.local && chmod a+rwx /.local
WORKDIR /jupyter

ARG PORT=8888
EXPOSE $PORT

RUN python -m ipykernel.kernelspec

CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter notebook --notebook-dir=/jupyter --port $PORT --ip 0.0.0.0 --no-browser --allow-root"]

FROM ml-base-${PACKAGE_OPTION} AS mlflow

RUN python -m pip install --no-cache-dir mlflow

ARG PORT=5000
EXPOSE $PORT

CMD ["mlflow", "server", "-h", "0.0.0.0", "-p", $PORT]
