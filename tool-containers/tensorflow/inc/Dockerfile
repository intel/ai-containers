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
ARG BASE_IMAGE_TAG=latest

FROM ${BASE_IMAGE_NAME}:${BASE_IMAGE_TAG} as inc

ARG PYTHON=python3.8

RUN apt-get update && apt-get install -y --no-install-recommends --fix-missing \
    libgl1-mesa-glx \
    libglib2.0-0

ARG INC_VER=1.12

ADD https://raw.githubusercontent.com/intel/neural-compressor/master/docker/third-party-programs-tensorflow.txt /licenses/
ADD https://raw.githubusercontent.com/intel/neural-compressor/v${INC_VER}/LICENSE /licenses/

ENV SIGOPT_PROJECT=.

RUN python -m pip install --no-cache-dir neural-compressor${INC_VER:+==${INC_VER}}
