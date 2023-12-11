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

wget https://torchserve.pytorch.org/mar_files/cat_dog_classification.mar
wget https://torchserve.pytorch.org/mar_files/dog_breed_classification.mar
wget https://raw.githubusercontent.com/pytorch/serve/master/examples/Workflows/dog_breed_classification/workflow_dog_breed_classification.yaml
wget https://raw.githubusercontent.com/pytorch/serve/master/examples/Workflows/dog_breed_classification/workflow_dog_breed_classification_handler.py
torch-workflow-archiver -f --workflow-name dog_breed_wf --spec-file workflow_dog_breed_classification.yaml --handler workflow_dog_breed_classification_handler.py --export-path /home/model-server/wf-store
[ -f "/home/model-server/wf-store/dog_breed_wf.war" ] && echo "dog_breed_wf.war Archived Succesfully at /home/model-server/wf-store/dog_breed_wf.war"
rm -rf cat_dog_classification.mar dog_breed_classification.mar workflow_dog_breed_classification_handler.py workflow_dog_breed_classification.yaml
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
