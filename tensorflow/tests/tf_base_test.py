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

import intel_extension_for_tensorflow as itex
import numpy as np
import tensorflow as tf

print(f"Tensorflow version {tf.__version__}")
print(f"Intel_Extension_for_TensorFlow version {itex.__version__}")

# Example taken from https://intel.github.io/intel-extension-for-tensorflow/latest/examples/quick_example.html#quick-example-py
# Conv + ReLU activation + Bias
N = 1
NUM_CHANNEL = 3
INPUT_WIDTH, INPUT_HEIGHT = (5, 5)
FILTER_WIDTH, FILER_HEIGHT = (2, 2)

x = np.random.rand(N, INPUT_WIDTH, INPUT_HEIGHT, NUM_CHANNEL).astype(np.float32)
weight = np.random.rand(FILTER_WIDTH, FILER_HEIGHT, NUM_CHANNEL, NUM_CHANNEL).astype(
    np.float32
)
bias = np.random.rand(NUM_CHANNEL).astype(np.float32)

conv = tf.nn.conv2d(x, weight, strides=[1, 1, 1, 1], padding="SAME")
activation = tf.nn.relu(conv)
result = tf.nn.bias_add(activation, bias)

print(result)
print("Finished")
