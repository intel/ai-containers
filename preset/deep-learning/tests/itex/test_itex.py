# Copyright (c) 2022 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================


#!/usr/bin/env python
# coding: utf-8


import tensorflow as tf
print("TensorFlow version {}".format(tf.__version__))

import tensorflow_hub as hub
from tensorflow.keras.applications.imagenet_utils import preprocess_input
import numpy as np

def load_data():
    x = np.random.rand(1,224,224,3)
    x = preprocess_input(x, mode='tf')
    x= x/2+ 0.5
    return x

import time

def main():
    gpus = tf.config.list_physical_devices('XPU')
    if gpus:
        print("Listing all GPUs:")
        print(gpus)
    cpus = tf.config.list_physical_devices('CPU')
    if cpus:
        print("Listing all CPUs:")
        print(cpus)
    module = hub.KerasLayer("https://tfhub.dev/google/supcon/resnet_v1_50/imagenet/classification/1")
    images = load_data()
    total = 0.0
    for i in range(100):
        s = time.time()
        logits = module(images)
        logits = tf.nn.softmax(logits)
        logits = logits.numpy()
        e = time.time()
        if i >=10:
            total += e - s
    print("Average time for inference: {:.2f} seconds".format(total/90.0))


if __name__ == "__main__":
    main()