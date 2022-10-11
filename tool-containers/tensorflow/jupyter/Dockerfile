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

FROM ${BASE_IMAGE_NAME}:${BASE_IMAGE_TAG} as jupyter

RUN python -m pip install --no-cache-dir jupyter matplotlib
# Pin ipykernel and nbformat; see https://github.com/ipython/ipykernel/issues/422
RUN python -m pip install --no-cache-dir jupyter_http_over_ws ipykernel nbformat
RUN jupyter serverextension enable --py jupyter_http_over_ws

RUN mkdir -p /tf-base/ && chmod -R a+rwx /tf-base/
RUN mkdir /.local && chmod a+rwx /.local
WORKDIR /tf-base
EXPOSE 8888

RUN python -m ipykernel.kernelspec

ADD third_party_programs.txt /licensing/jupyter_third_party_programs.txt

CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter notebook --notebook-dir=${WORKDIR} --ip 0.0.0.0 --no-browser --allow-root"]
