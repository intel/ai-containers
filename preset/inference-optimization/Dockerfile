# Copyright (c) 2024 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

ARG COMPOSE_PROJECT_NAME
FROM ${COMPOSE_PROJECT_NAME}-dl-base as inference-optimization

ENV SIGOPT_PROJECT=.

ARG NEURAL_COMPRESSOR_VERSION
ARG INTEL_CHANNEL


RUN conda install -yn pytorch-cpu -c "${INTEL_CHANNEL}" -c conda-forge \
        neural-compressor="${NEURAL_COMPRESSOR_VERSION}"

RUN conda install -yn pytorch-gpu -c "${INTEL_CHANNEL}" -c conda-forge \
        neural-compressor="${NEURAL_COMPRESSOR_VERSION}"

RUN conda install -yn tensorflow-cpu -c "${INTEL_CHANNEL}" -c conda-forge \
        neural-compressor="${NEURAL_COMPRESSOR_VERSION}"

RUN conda install -yn tensorflow-gpu -c "${INTEL_CHANNEL}" -c conda-forge \
        neural-compressor="${NEURAL_COMPRESSOR_VERSION}"

RUN conda run -n tensorflow-cpu python -m pip install --no-deps --no-cache-dir \
        'tf2onnx>=1.16.1' \
        'onnxruntime>=1.17.3' && \
    conda clean -y --all

RUN conda run -n tensorflow-gpu python -m pip install --no-deps --no-cache-dir \
        'tf2onnx>=1.16.1' \
        'onnxruntime>=1.17.3' && \
    conda clean -y --all

COPY --chown=dev notebooks /home/dev/jupyter
COPY --chown=dev tests /home/dev/sample-tests
