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

ARG PACKAGE_OPTION=pip

ARG COMPOSE_PROJECT_NAME
FROM ${COMPOSE_PROJECT_NAME}-python AS ml-base-pip

ARG SCIKIT_VERSION
ARG XGBOOST_VERSION

RUN python -m pip install --no-cache-dir \
    daal4py \
    matplotlib \
    scikit-learn-intelex${SCIKIT_VERSION:+==${SCIKIT_VERSION}} \
    threadpoolctl \
    xgboost${XGBOOST_VERSION:+==${XGBOOST_VERSION}}

COPY base/.patch_sklearn.py ${HOME}/.patch_sklearn.py

RUN mkdir -p /licensing && \
	wget -O - https://github.com/intel/scikit-learn-intelex/archive/refs/tags/${SCIKIT_VERSION}.tar.gz | \
	tar -xz -C /licensing --strip=2 "scikit-learn-intelex-${SCIKIT_VERSION}/doc/third-party-programs-sklearnex.txt" \
	"scikit-learn-intelex-${SCIKIT_VERSION}/doc/daal4py/third-party-programs.txt"

RUN curl --insecure https://raw.githubusercontent.com/intel/scikit-learn-intelex/${SCIKIT_VERSION}/LICENSE -o /licensing/SCIKIT_LICENSE

FROM ${COMPOSE_PROJECT_NAME}-python AS ml-base-idp

ARG SCIKIT_VERSION
ARG XGBOOST_VERSION

ENV BASH_ENV /root/.bash_profile

RUN python -m pip install --no-cache-dir --ignore-installed \
    daal4py \
    matplotlib \
    # https://github.com/intel/scikit-learn-intelex/blob/master/requirements-test.txt
    numpy==1.23.0 \ 
    scikit-learn-intelex${SCIKIT_VERSION:+==${SCIKIT_VERSION}} \
    threadpoolctl \
    xgboost${XGBOOST_VERSION:+==${XGBOOST_VERSION}} && \
    apt-get clean && conda clean -y --all

ENV PYTHONSTARTUP=${HOME}/.patch_sklearn.py
COPY base/.patch_sklearn.py ${HOME}/.patch_sklearn.py

RUN mkdir -p /licensing && \
	wget -O - https://github.com/intel/scikit-learn-intelex/archive/refs/tags/${SCIKIT_VERSION}.tar.gz | \
	tar -xz -C /licensing --strip=2 "scikit-learn-intelex-${SCIKIT_VERSION}/doc/third-party-programs-sklearnex.txt" \
	"scikit-learn-intelex-${SCIKIT_VERSION}/doc/daal4py/third-party-programs.txt"

RUN curl --insecure https://raw.githubusercontent.com/intel/scikit-learn-intelex/${SCIKIT_VERSION}/LICENSE -o /licensing/SCIKIT_LICENSE

FROM ml-base-${PACKAGE_OPTION} AS jupyter

RUN python -m pip install --no-cache-dir jupyterlab jupyterhub notebook jupyter-server-proxy

RUN mkdir -p /jupyter/ && chmod -R a+rwx /jupyter/
RUN mkdir /.local && chmod a+rwx /.local
WORKDIR /jupyter

ARG PORT=8888
EXPOSE $PORT

CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter notebook --notebook-dir=/jupyter --port $PORT --ip 0.0.0.0 --no-browser --allow-root"]

FROM ml-base-${PACKAGE_OPTION} AS mlflow

RUN python -m pip install --no-cache-dir mlflow

ARG PORT=5000
EXPOSE $PORT

CMD ["mlflow", "server", "-h", "0.0.0.0", "-p", $PORT]
