#!/bin/bash

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

set -e

apt-get -y update
apt-get -y install curl jq

echo 'Testing if server is running'
curl --fail -s -X GET http://localhost:8888/api/status
echo ''

echo 'Test if oneapi-sample was downloaded'
if [[ $(curl --fail -s -X GET http://localhost:8888/api/contents | jq -r '.content[] | select(.name=="oneapi-sample.ipynb")') ]]; then
    echo 'oneapi-sample.ipynb was downloaded'
else
    echo 'oneapi-sample.ipynb was not downloaded'
fi
