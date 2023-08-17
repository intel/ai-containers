#! /bin/bash
source activate classical-ml

set -xe
mkdir -p ~/data
python ${WORKSPACE:-preset/classical-ml/tests/modin}/modin_quickstart.py
