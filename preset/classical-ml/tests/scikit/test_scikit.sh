#! /bin/bash
source activate classical-ml

set -xe
SCRIPT_DIR="$(dirname $0)"

python ${SCRIPT_DIR}/kmeans.py

python ${SCRIPT_DIR}/kmeans.py true
