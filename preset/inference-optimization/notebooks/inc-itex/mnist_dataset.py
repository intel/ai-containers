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
# tf 2.x
import tensorflow as tf
from tensorflow.keras import utils


def read_data():
    classes = 10
    print("Loading data ...")
    mnist = tf.keras.datasets.mnist.load_data()
    # print("Converting data ...")

    (x_train, label_train), (x_test, label_test) = mnist

    x_train = x_train.astype("float32")
    x_test = x_test.astype("float32")
    x_train = x_train / 255.0
    x_test = x_test / 255.0

    y_train = utils.to_categorical(label_train, classes)
    y_test = utils.to_categorical(label_test, classes)

    x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], x_train.shape[2], 1)
    x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], x_test.shape[2], 1)

    print("Done")
    return x_train, y_train, label_train, x_test, y_test, label_test
