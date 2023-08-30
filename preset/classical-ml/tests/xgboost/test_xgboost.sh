#! /bin/bash

source activate classical-ml
mkdir -p ~/data
mkdir -p ~/output

set -xe
wget https://raw.githubusercontent.com/dmlc/xgboost/master/demo/data/agaricus.txt.train -q -O ~/data/agaricus.txt.train
wget https://raw.githubusercontent.com/dmlc/xgboost/master/demo/data/agaricus.txt.test -q -O ~/data/agaricus.txt.test
wget https://raw.githubusercontent.com/dmlc/xgboost/master/demo/data/featmap.txt -q -O ~/data/featmap.txt

SCRIPT_DIR="$(dirname $0)"
python ${SCRIPT_DIR}/test_xgboost.py
