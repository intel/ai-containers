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

import time

from sklearn import metrics
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearnex import patch_sklearn

x, y = fetch_openml(name="a9a", return_X_y=True)

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

patch_sklearn()
from sklearn.svm import SVC

params = {"C": 100.0, "kernel": "rbf", "gamma": "scale"}
start = time.time()
classifier = SVC(**params).fit(x_train, y_train)
train_patched = time.time() - start
print(f"Intel® extension for Scikit-learn time: {train_patched:.2f} s")

predicted = classifier.predict(x_test)
report = metrics.classification_report(y_test, predicted)
print(f"Classification report for Intel® extension for Scikit-learn SVC:\n{report}\n")

from sklearnex import unpatch_sklearn

unpatch_sklearn()
from sklearn.svm import SVC

start = time.time()
classifier = SVC(**params).fit(x_train, y_train)
train_unpatched = time.time() - start
print(f"Original Scikit-learn time: {train_unpatched:.2f} s")

predicted = classifier.predict(x_test)
report = metrics.classification_report(y_test, predicted)
print(f"Classification report for original Scikit-learn SVC:\n{report}\n")

speedup = train_unpatched / train_patched
print(f"Speedup with Intel® extension for Scikit-learn on SVC task:{speedup}")
