#!/bin/bash

conda activate tensorflow
set -xe

mkdir -p ~/input_model #User might not have write permission to write at root of MLOps repo
wget https://storage.googleapis.com/intel-optimized-tensorflow/models/v1_6/mobilenet_v1_1.0_224_frozen.pb -O ~/input_model/mobilenet_v1_1.0_224_frozen.pb
SCRIPT_DIR="$(dirname $0)"
python ${SCRIPT_DIR}/test_inc.py --device $1 --workspace ~/nc_workspace
