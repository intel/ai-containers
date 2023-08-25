#! /bin/bash
source activate classical-ml

set -xe
python ${WORKSPACE:-preset/classical-ml/tests/scikit}/kmeans.py

python ${WORKSPACE:-preset/classical-ml/tests/scikit}/kmeans.py true