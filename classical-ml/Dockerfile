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

ARG REGISTRY
ARG REPO
ARG GITHUB_RUN_NUMBER
ARG BASE_IMAGE_NAME
ARG BASE_IMAGE_TAG
ARG PACKAGE_OPTION=pip
ARG PYTHON_VERSION
ARG PYTHON_BASE=${REGISTRY}/${REPO}:b-${GITHUB_RUN_NUMBER}-${BASE_IMAGE_NAME}-${BASE_IMAGE_TAG}-${PACKAGE_OPTION}-py${PYTHON_VERSION}-base
FROM ${PYTHON_BASE} AS ml-base-pip

WORKDIR /
COPY requirements.txt .

RUN python -m pip install --no-cache-dir \
    --ignore-installed -r requirements.txt

COPY base/.patch_sklearn.py ${HOME}/.patch_sklearn.py

RUN mkdir -p /licensing && \
    wget --progress=dot:giga -O - "https://github.com/intel/scikit-learn-intelex/archive/refs/heads/main.tar.gz" | \
    tar -xz -C /licensing --strip=2 "scikit-learn-intelex-main/doc/third-party-programs-sklearnex.txt" \
    "scikit-learn-intelex-main/doc/daal4py/third-party-programs.txt"

RUN wget --progress=dot:giga --no-check-certificate "https://raw.githubusercontent.com/intel/scikit-learn-intelex/main/LICENSE" -O /licensing/SCIKIT_LICENSE

FROM ${PYTHON_BASE} AS ml-base-idp

ENV BASH_ENV /root/.bash_profile

WORKDIR /
COPY requirements.txt .

RUN python -m pip install --no-cache-dir \
    --ignore-installed -r requirements.txt  && \
    apt-get clean && conda clean -y --all

ENV PYTHONSTARTUP=${HOME}/.patch_sklearn.py
COPY base/.patch_sklearn.py ${HOME}/.patch_sklearn.py

RUN mkdir -p /licensing && \
    wget --progress=dot:giga -O - "https://github.com/intel/scikit-learn-intelex/archive/refs/heads/main.tar.gz" | \
    tar -xz -C /licensing --strip=2 "scikit-learn-intelex-main/doc/third-party-programs-sklearnex.txt" \
    "scikit-learn-intelex-main/doc/daal4py/third-party-programs.txt"

RUN wget --progress=dot:giga --no-check-certificate "https://raw.githubusercontent.com/intel/scikit-learn-intelex/main/LICENSE" -O /licensing/SCIKIT_LICENSE

FROM ml-base-${PACKAGE_OPTION} AS jupyter

WORKDIR /jupyter
COPY jupyter-requirements.txt .

RUN python -m pip install --no-cache-dir -r jupyter-requirements.txt

RUN mkdir -p /jupyter/ && chmod -R a+rwx /jupyter/
RUN mkdir /.local && chmod a+rwx /.local

EXPOSE 8888

CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter notebook --notebook-dir=/jupyter --port 8888 --ip 0.0.0.0 --no-browser --allow-root --ServerApp.token= --ServerApp.password= --ServerApp.allow_origin=* --ServerApp.base_url=$NB_PREFIX"]
