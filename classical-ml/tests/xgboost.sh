# Copyright (c) 2022 Intel Corporation
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
# ============================================================================
#
# This file was assembled from multiple pieces, whose use is documented
# throughout. Please refer to the TensorFlow dockerfiles documentation
# for more information.
# based on https://github.com/pytorch/pytorch/blob/master/Dockerfile
#
# NOTE: To build this you will need a docker version >= 19.03 and DOCKER_BUILDKIT=1
#
#       If you do not use buildkit you are not going to have a good time
#
#       For reference:
#           https://docs.docker.com/develop/develop-images/build_enhancements/

#!/bin/bash

mkdir -p /home/dev/data /home/dev/output
cd /home/dev/data
wget https://raw.githubusercontent.com/dmlc/xgboost/master/demo/data/agaricus.txt.train
wget https://raw.githubusercontent.com/dmlc/xgboost/master/demo/data/agaricus.txt.test
wget https://raw.githubusercontent.com/dmlc/xgboost/master/demo/data/featmap.txt
cd ..

wget https://raw.githubusercontent.com/intel/ai-containers/main/preset/classical-ml/tests/xgboost/test_xgboost.py
python test_xgboost.py

rm -rf /home/dev