#!/bin/bash

conda activate tensorflow
set -xe

mkdir -p ~/onnx_test 
SCRIPT_DIR="$(dirname $0)"

python ${SCRIPT_DIR}/test_onnx.py
