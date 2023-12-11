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
# curl -O https://torchserve.pytorch.org/mar_files/squeezenet1_1.mar
curl --fail -O https://raw.githubusercontent.com/pytorch/serve/master/docs/images/kitten_small.jpg
curl --fail -X GET http://localhost:8080/ping
curl --fail -X POST "http://localhost:8081/models?initial_workers=1&synchronous=true&url=/home/model-server/model-store/squeezenet1_1.mar&model_name=squeezenet"
curl --fail -X POST http://127.0.0.1:8080/v2/models/squeezenet/infer -T /home/model-server/model-store/kitten_small.jpg
rm -rf /home/model-server/model-store/squeezenet1_1.mar kitten_small.jpg
