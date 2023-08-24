#
# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 Intel Corporation
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
#
#

from neural_compressor.config import PostTrainingQuantConfig
from neural_compressor.data import DataLoader
from neural_compressor.data import Datasets
from neural_compressor.quantization import fit
from neural_compressor.utils.utility import set_workspace

from torchvision.models import resnet18, ResNet18_Weights

def main(args):

    # Built-in dummy dataset
    set_workspace(args.workspace)
    dataset = Datasets('pytorch')['dummy'](shape=(1, 3, 224, 224))
    # Built-in calibration dataloader and evaluation dataloader for Quantization.
    dataloader = DataLoader(framework='pytorch', dataset=dataset)
    # Post Training Quantization Config
    config = PostTrainingQuantConfig(args.device, backend='ipex')
    model = resnet18(weights=ResNet18_Weights.DEFAULT).to(args.device)
    # Just call fit to do quantization.
    q_model = fit(model=model,
                  conf=config,
                  calib_dataloader=dataloader)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', default='cpu', choices=['cpu', 'xpu'])
    parser.add_argument('--workspace', required=True)
    args = parser.parse_args()
    main(args)