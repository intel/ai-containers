#! /bin/bash

# Copyright (c) 2024 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

mkdir -p ~/data
mkdir -p ~/output

set -xe
wget https://raw.githubusercontent.com/dmlc/xgboost/master/demo/data/agaricus.txt.train -q -O ~/data/agaricus.txt.train
wget https://raw.githubusercontent.com/dmlc/xgboost/master/demo/data/agaricus.txt.test -q -O ~/data/agaricus.txt.test
wget https://raw.githubusercontent.com/dmlc/xgboost/master/demo/data/featmap.txt -q -O ~/data/featmap.txt

SCRIPT_DIR=$(dirname "$0")
python "${SCRIPT_DIR}/test_xgboost.py"
