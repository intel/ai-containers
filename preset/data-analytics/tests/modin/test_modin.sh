#! /bin/bash
source activate data-analytics

set -xe
mkdir -p ~/data
python ${WORKSPACE:-preset/classical-ml/tests/modin}/modin_quickstart.py
