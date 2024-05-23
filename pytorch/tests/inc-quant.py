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

from neural_compressor.config import PostTrainingQuantConfig
from neural_compressor.data import DataLoader, Datasets
from neural_compressor.quantization import fit

# pylint: skip-file
from torchvision import models

float_model = models.resnet18()
dataset = Datasets("pytorch")["dummy"](shape=(1, 3, 224, 224))
calib_dataloader = DataLoader(framework="pytorch", dataset=dataset)
static_quant_conf = PostTrainingQuantConfig()
quantized_model = fit(
    model=float_model, conf=static_quant_conf, calib_dataloader=calib_dataloader
)
