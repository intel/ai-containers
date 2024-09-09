#!/usr/bin/env bash

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

# Load bash libraries
SCRIPT_DIR=${APP_ROOT}/bin
# shellcheck disable=SC1091
source "${SCRIPT_DIR}"/utils/process.sh

if [ -f "${SCRIPT_DIR}/utils/setup-elyra.sh" ]; then
	# shellcheck disable=SC1091
	source "${SCRIPT_DIR}"/utils/setup-elyra.sh
fi

# Initialize notebooks arguments variable
NOTEBOOK_PROGRAM_ARGS=""

# Set default ServerApp.port value if NOTEBOOK_PORT variable is defined
if [ -n "${NOTEBOOK_PORT}" ]; then
	NOTEBOOK_PROGRAM_ARGS+="--ServerApp.port=${NOTEBOOK_PORT} "
fi

# Set default ServerApp.base_url value if NOTEBOOK_BASE_URL variable is defined
if [ -n "${NOTEBOOK_BASE_URL}" ]; then
	NOTEBOOK_PROGRAM_ARGS+="--ServerApp.base_url=${NOTEBOOK_BASE_URL} "
fi

# Set default ServerApp.root_dir value if NOTEBOOK_ROOT_DIR variable is defined
if [ -n "${NOTEBOOK_ROOT_DIR}" ]; then
	NOTEBOOK_PROGRAM_ARGS+="--ServerApp.root_dir=${NOTEBOOK_ROOT_DIR} "
else
	NOTEBOOK_PROGRAM_ARGS+="--ServerApp.root_dir=${HOME} "
fi

# Add additional arguments if NOTEBOOK_ARGS variable is defined
if [ -n "${NOTEBOOK_ARGS}" ]; then
	NOTEBOOK_PROGRAM_ARGS+=${NOTEBOOK_ARGS}
fi

echo "${NOTEBOOK_PROGRAM_ARGS}"

# Start the JupyterLab notebook
# shellcheck disable=SC2086
start_process jupyter lab ${NOTEBOOK_PROGRAM_ARGS} \
	--ServerApp.ip=0.0.0.0 \
	--ServerApp.allow_origin="*" \
	--ServerApp.open_browser=False
