#!/usr/bin/env bash
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
# SPDX-License-Identifier: Apache-2.0

# Create a temp virtualenv to install huggingface datasets API
VENV_DIR='hf_venv'

python3 -m venv $VENV_DIR

# Activate the venv and install datasets API
source $VENV_DIR/bin/activate && pip install --no-cache datasets

# Run the following python code to download and save a subset of financial alpaca dataset
echo -e "
import os
from datasets import load_dataset

dataset_dir = os.environ.get('DATASET_DIR', '/tmp/dataset')

dataset = load_dataset('gbharti/finance-alpaca',
            split='train[:17153]')

dataset.to_json(os.path.join(dataset_dir, 'financial-alpaca.json'))
" | $VENV_DIR/bin/python3

# Delete the venv
rm -rf $VENV_DIR

echo "Dataset saved as \"$DATASET_DIR/financial-alpaca.json\""
