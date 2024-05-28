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
# pylint: skip-file
import sys

import tensorflow as tf
from tensorflow.python.client import device_lib

print(tf.__version__)


def get_available_gpus():
    """Import Test"""
    local_device_protos = device_lib.list_local_devices()
    print(local_device_protos)
    devices = [x.name for x in local_device_protos if x.device_type == "XPU"]
    for i in devices:
        if "XPU" in i:
            return True
    return False


IS_XPU = get_available_gpus()
if not IS_XPU:
    print("Intel GPU not detected. Please install GPU with compatible drivers")
    sys.exit(1)
