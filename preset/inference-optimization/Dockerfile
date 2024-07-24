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

SHELL ["/bin/bash", "-c"]

ENV SIGOPT_PROJECT=.
ARG NEURAL_COMPRESSOR_VERSION
ARG INTEL_CHANNEL


RUN ENVS_LIST=('pytorch-cpu' 'pytorch-gpu' 'tensorflow-cpu' 'tensorflow-gpu') && \
    for i in "${!ENVS_LIST[@]}"; do \
        CONDA_ENV="${ENVS_LIST[i]}" && \
        conda install -yn "$CONDA_ENV" \
        -c "https://$USER_AF:$PASS_AF@af01p-fm.devtools.intel.com/artifactory/aitools-conda_channel-fm-local" \
        -c "https://$USER_AF:$PASS_AF@af01p-fm.devtools.intel.com/artifactory/api/conda/aitools-conda_channel-fm-local/intel-2024.2.0" \
        "neural-compressor=${NEURAL_COMPRESSOR_VERSION}" \
        ; \
    done && \
    conda clean -y --all

RUN ENVS_LIST=('tensorflow-cpu' 'tensorflow-gpu') && \
    for i in "${!ENVS_LIST[@]}"; do \
        CONDA_ENV="${ENVS_LIST[i]}" && \
        conda run -n "$CONDA_ENV" python -m pip install --no-deps --no-cache-dir \
        'tf2onnx==1.16.1' \
        'onnxruntime==1.18.1' \
        ; \
    done && \
    conda clean -y --all

COPY --chown=dev notebooks /home/dev/jupyter
COPY --chown=dev tests /home/dev/sample-tests
