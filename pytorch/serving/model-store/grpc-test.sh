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
curl --fail -O https://raw.githubusercontent.com/pytorch/serve/95cdec66a93eefca00d0a1f4939369636a13a33e/examples/image_classifier/kitten.jpg
curl --fail -O https://raw.githubusercontent.com/pytorch/serve/95cdec66a93eefca00d0a1f4939369636a13a33e/frontend/server/src/main/resources/proto/inference.proto
curl --fail -O https://raw.githubusercontent.com/pytorch/serve/95cdec66a93eefca00d0a1f4939369636a13a33e/frontend/server/src/main/resources/proto/management.proto
curl --fail -O https://torchserve.s3.amazonaws.com/mar_files/densenet161.mar
python -m pip install -r requirements.txt
python -m grpc_tools.protoc --proto_path=/home/model-server/model-store --python_out=. --grpc_python_out=. inference.proto management.proto
curl --fail -X POST "http://localhost:8081/models?initial_workers=1&synchronous=true&url=/home/model-server/model-store/densenet161.mar&model_name=densenet161"
python torchserve_grpc_client.py infer densenet161 kitten.jpg
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
rm -rf kitten.jpg inference.proto management.proto inference_pb* management_pb* densenet161.mar
