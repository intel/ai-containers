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
# THIS IS A GENERATED DOCKERFILE.
#
# This file was assembled from multiple pieces, whose use is documented
# throughout. Please refer to the TensorFlow dockerfiles documentation
# for more information.

ARG BASE_IMAGE_NAME=tf-base
ARG BASE_IMAGE_TAG=mpi

FROM ${BASE_IMAGE_NAME}:${BASE_IMAGE_TAG} as base

FROM base as dev

ARG DEBIAN_FRONTEND="noninteractive"

# Install Horovod
ARG HOROVOD_WITHOUT_PYTORCH=1
ARG HOROVOD_WITHOUT_MXNET=1
ARG HOROVOD_WITH_TENSORFLOW=1
ARG HOROVOD_VERSION=v0.24.3

RUN apt-get update && apt-get install -y --no-install-recommends --fix-missing \
    build-essential \
    cmake \
    g++ \
    gcc \
    git \
    python3-dev

RUN python -m pip install git+https://github.com/horovod/horovod.git@${HOROVOD_VERSION}

FROM base as prod

ARG PYTHON=python3.8

COPY --from=dev /usr/local/lib/${PYTHON}/dist-packages /usr/local/lib/${PYTHON}/dist-packages
