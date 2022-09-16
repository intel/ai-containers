# Copyright (c) 2022 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

ARG BASE_IMAGE_NAME=ipex-base
ARG BASE_IMAGE_TAG=mpi
ARG PACKAGE_OPTION=idp
ARG BASE_OS_NAME=debian

FROM ${BASE_IMAGE_NAME}-${BASE_OS_NAME}-${PACKAGE_OPTION}:${BASE_IMAGE_TAG} as base

FROM base as dev

ARG DEBIAN_FRONTEND="noninteractive"

# Install Horovod
ARG HOROVOD_WITHOUT_MXNET=0
ARG HOROVOD_WITHOUT_TENSORFLOW=0
ARG HOROVOD_WITH_PYTORCH=1
ARG HOROVOD_VERSION=v0.24.3

RUN apt-get update && apt-get install -y --no-install-recommends --fix-missing \
    build-essential \
    cmake \
    g++ \
    gcc \
    git \
    python3-dev

RUN python -m pip install git+https://github.com/horovod/horovod.git@${HOROVOD_VERSION}

# FROM base as prod
#
# ARG PYTHON=python3.8
#
# COPY --from=dev /usr/local/lib/${PYTHON}/dist-packages /usr/local/lib/${PYTHON}/dist-packages
