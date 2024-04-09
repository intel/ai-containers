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
import argparse

import intel_extension_for_pytorch as ipex
import torch
import torchvision.models as models

parser = argparse.ArgumentParser()
parser.add_argument("--device", default="cpu", choices=["cpu", "xpu"])
parser.add_argument("--ipex", action="store_true")
args = parser.parse_args()

model = models.resnet50(weights="ResNet50_Weights.DEFAULT")
model.eval()
data = torch.rand(1, 3, 224, 224)

model = model.to(args.device)
data = data.to(args.device)
print("Choosing device: {}".format(args.device))

if args.ipex:
    model = ipex.optimize(model)
    print("Applying IPEX Optimization")

import time

with torch.no_grad():
    # Warmup
    for i in range(100):
        model(data)

    # Profiling
    total = 0.0
    for i in range(100):
        start = time.time()
        model(data)
        end = time.time()
        total += end - start
    print("Average Inference Time: {} seconds".format(total / 100.0))
