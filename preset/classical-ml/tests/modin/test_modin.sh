#! /bin/bash
source activate classical-ml

set -xe
mkdir -p /home/dev/data
python ${WORKSPACE:-preset/classical-ml/tests/modin}/modin_quickstart.py
