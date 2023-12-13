# Taken from https://github.com/onnx/tensorflow-onnx/blob/main/examples/end2end_tfhub.py
# SPDX-License-Identifier: Apache-2.0

"""
This example retrieves a model from tensorflowhub.
It is converted into ONNX. Predictions are compared to
the predictions from tensorflow to check there is no
discrepencies. Inferencing time is also compared between
*onnxruntime*, *tensorflow* and *tensorflow.lite*.
"""
from onnxruntime import InferenceSession
import os
import sys
import subprocess
import timeit
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Input
try:
    import tensorflow_hub as tfhub
except ImportError:
    # no tensorflow_hub
    print("tensorflow_hub not installed.")
    sys.exit(0)

home_dir=os.path.expanduser('~')

########################################
# Downloads the model.
hub_layer = tfhub.KerasLayer(
    "https://tfhub.dev/google/efficientnet/b0/classification/1")
model = keras.Sequential()
model.add(Input(shape=(224, 224, 3), dtype=tf.float32))
model.add(hub_layer)
print(model.summary())

########################################
# Saves the model.
input_model_path = os.path.join(home_dir, "efficientnetb0clas")
if not os.path.exists(input_model_path):
    os.mkdir(input_model_path)
tf.keras.models.save_model(model, input_model_path)

input_names = [n.name for n in model.inputs]
output_names = [n.name for n in model.outputs]
print('inputs:', input_names)
print('outputs:', output_names)

########################################
# Testing the model.
input = np.random.randn(2, 224, 224, 3).astype(np.float32)
expected = model.predict(input)
print(expected)

########################################
# Run the command line.
proc = subprocess.run(
    'python -m tf2onnx.convert --saved-model {} --output {}.onnx --opset 12'.format(input_model_path,input_model_path).split(),
    capture_output=True)
print(proc.returncode)
print(proc.stdout.decode('ascii'))
print(proc.stderr.decode('ascii'))

########################################
# Runs onnxruntime.
session = InferenceSession("{}.onnx".format(input_model_path))
got = session.run(None, {'input_1': input})
print(got[0])

########################################
# Measures the differences.
print(np.abs(got[0] - expected).max())

########################################
# Measures processing time.
print('tf:', timeit.timeit('model.predict(input)',
                           number=10, globals=globals()))
print('ort:', timeit.timeit("session.run(None, {'input_1': input})",
                            number=10, globals=globals()))