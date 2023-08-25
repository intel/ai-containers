#!/bin/bash

conda activate tensorflow
set -xe

mkdir -p ~/onnx_test #User might not have write permission to write at root of MLOps repo
SCRIPT_DIR="$(dirname $0)"

python ${SCRIPT_DIR}/test_onnx.py
