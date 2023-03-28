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

ARG DEBIAN_FRONTEND="noninteractive"

RUN apt-get install --no-install-recommends --fix-missing curl -y

ARG ONECCL_VERSION=1.12.0
ARG ONECCL_URL=https://developer.intel.com/ipex-whl-stable-cpu

RUN curl https://raw.githubusercontent.com/oneapi-src/oneCCL/b7d66de16e17f88caffd7c6df4cd5e12b266af84/third-party-programs.txt -o /licensing/oneccl_third_party_programs.txt 

RUN python -m pip install --no-cache-dir oneccl_bind_pt==${ONECCL_VERSION} -f ${ONECCL_URL}
