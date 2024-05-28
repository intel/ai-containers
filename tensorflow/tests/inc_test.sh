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
git clone https://github.com/intel/neural-compressor.git
cd neural-compressor/examples/tensorflow/nlp/bert_large_squad/quantization/ptq || exit
bash prepare_dataset.sh --output_dir=./data

# Preprocess the dataset
python create_tf_record.py --vocab_file=./data/vocab.txt --predict_file=./data/dev-v1.1.json --output_file=./data/eval.tf_record

# Download model
bash prepare_model.sh --output_dir=./model
python freeze_estimator_to_pb.py --input_model=./model --output_model=./bert_fp32.pb

#Run quantization using INC
bash run_quant.sh --input_model=./bert_fp32.pb --output_model=./bert_int8.pb --dataset_location=./data

#Run tests on quantized model
# bash run_benchmark.sh --input_model=./bert_squad_int8.pb --mode=performance --dataset_location=./data --batch_size=64
# bash run_benchmark.sh --input_model=./bert_int8.pb --mode=accuracy --dataset_location=./data --batch_size=64
