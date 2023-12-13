#!/bin/bash

conda activate $1
set -xe

mkdir -p ~/input_model #User might not have write permission to write at root of MLOps repo
SCRIPT_DIR="$(dirname $0)"
python ${SCRIPT_DIR}/test_inc.py --device $2 --workspace ~/nc_workspace
