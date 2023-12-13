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

apt-get -y update
apt-get -y install curl

curl --fail -X GET http://localhost:8080/ping

cd ../model-store
curl --fail -O https://torchserve.pytorch.org/mar_files/cat_dog_classification.mar
curl --fail -O https://torchserve.pytorch.org/mar_files/dog_breed_classification.mar
curl --fail -X POST "http://127.0.0.1:8081/models?url=cat_dog_classification.mar"
curl --fail -X POST "http://127.0.0.1:8081/models?url=dog_breed_classification.mar"

cd ../wf-store
curl --fail -X POST "http://127.0.0.1:8081/workflows?url=dog_breed_wf.war"

curl --fail -O https://raw.githubusercontent.com/pytorch/serve/master/examples/Workflows/dog_breed_classification/model_input/Cat.jpg
curl --fail -X POST http://127.0.0.1:8080/wfpredict/dog_breed_wf -T Cat.jpg
curl --fail -O https://raw.githubusercontent.com/pytorch/serve/master/examples/Workflows/dog_breed_classification/model_input/Dog1.jpg
curl --fail -X POST http://127.0.0.1:8080/wfpredict/dog_breed_wf -T Dog1.jpg
curl --fail -O https://raw.githubusercontent.com/pytorch/serve/master/examples/Workflows/dog_breed_classification/model_input/Dog2.jpg
curl --fail -X POST http://127.0.0.1:8080/wfpredict/dog_breed_wf -T Dog2.jpg

rm -rf *.war Cat.jpg Dog1.jpg Dog2.jpg ../model-store/*.mar
