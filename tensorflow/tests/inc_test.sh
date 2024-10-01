#!/bin/bash

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

# Prepare dataset
rm -rf neural-compressor || true
git clone https://github.com/intel/neural-compressor.git
cd neural-compressor/examples/tensorflow/nlp/bert_large_squad/quantization/ptq || exit 1

echo "Preparing the dataset"
bash prepare_dataset.sh --output_dir="$PWD"/data

# Preprocess the dataset
echo "Preprocessing the dataset"
python create_tf_record.py --vocab_file=data/vocab.txt --predict_file=data/dev-v1.1.json --output_file=./eval.tf_record

echo "Preparing the model"
bash prepare_model.sh --output_dir="$PWD"/model

# Run quantization using INC
echo "Running quantization"
bash run_quant.sh --input_model=./bert_fp32.pb --output_model=./bert_int8.pb --dataset_location=./eval.tf_record

cd - || exit 1
rm -rf neural-compressor || true
