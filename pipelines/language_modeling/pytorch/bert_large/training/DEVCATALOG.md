# **Document Level Sentiment Analysis Using Hugging Face Transformers - Training**

## **Use Hugging Face API for Natural Language Processing Tasks**
DLSA is Intel optimized representative End-to-end Fine-Tuning & Inference pipeline for Document level sentiment analysis using BERT model implemented with Hugging Face transformer API. For detailed information about the workflow, go to [Document Level Sentiment Analysis](https://github.com/intel/document-level-sentiment-analysis) GitHub repository.

## **Pull Docker Image**
```
docker pull intel/hugging-face-dlsa:training-intel-optimized-pytorch-latest
```

## **Download Model**
Clone [End-to-End DLSA](https://github.com/intel/document-level-sentiment-analysis) repository into your working directory.
```
git clone https://github.com/intel/document-level-sentiment-analysis.git .
git checkout dlsa_multinode_ipex_v1.2
```

## **Download Dataset**
### **SST-2 dataset**
Download and extract SST-2 dataset
```
wget https://dl.fbaipublicfiles.com/glue/data/SST-2.zip && unzip SST-2.zip && mv SST-2 sst
```
### **IMDB dataset**
Download and extract IMDB dataset
```
wget http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz && tar -zxf aclImdb_v1.tar.gz
```
### **Prepare dataset**
Set dataset directory 

For SST-2 dataset
```
export DATASET_DIR=$(pwd)/sst
```
For IMDB dataset
```
export DATASET_DIR=$(pwd)/aclImdb
```
Copy dataset
```
mkdir -p profiling-transformers/datasets && cp -r ${DATASET_DIR} profiling-transformers/datasets
```

## **Customization Options**
| Script Name | Description | 
| --- | --- |
| DATASET | `sst2` and `imdb`. Names of datasets. For SST-2 dataset, use `DATASET=sst2` and for IMDB dataset, use `DATASET=imdb` | 
| MODEL | `bert-large-uncased`. Name of model on [Hugging Face](https://huggingface.co/) | 

## **Running with Docker**
The snippet below shows a quick start running with the following options: `DATASET=sst2` and `OUTPUT_DIR=/output`.

```
export DATASET=sst2
export MODEL=bert-large-uncased
export OUTPUT_DIR=/output

docker run \
  --env DATASET=${DATASET} \
  --env MODEL_NAME_OR_PATH=${MODEL} \
  --env ${OUTPUT_DIR}:${OUTPUT_DIR}/fine_tuned \
  --env http_proxy=${http_proxy} \
  --env https_proxy=${https_proxy} \
  --env no_proxy=${no_proxy} \
  --volume ${OUTPUT_DIR}:${OUTPUT_DIR} \
  --volume ${PWD}:/workspace \
  --workdir /workspace/profiling-transformers \
  --privileged --init -it \
  intel/hugging-face-dlsa:training-intel-optimized-pytorch-latest \
  fine-tuning/run_dist.sh -np 1 -ppn 1 fine-tuning/run_ipex_native.sh
```

## **Documentation and Sources**

### **Get Started**
[Docker* Repository](https://hub.docker.com/u/intel) <br>
[Main GitHub*](https://github.com/intel/document-level-sentiment-analysis)<br>
[Readme](https://github.com/intel/document-level-sentiment-analysis/blob/main/README.md)<br>
[Release Notes]()<br>

### **Code Sources**
[Dockerfile](https://github.com/intel-innersource/frameworks.ai.infrastructure.machine-learning-operations/blob/develop/pipelines/language_modeling/pytorch/bert_large/training/Dockerfile.hugging-face-dlsa)<br>
[Report Issue](https://community.intel.com/t5/Intel-Optimized-AI-Frameworks/bd-p/optimized-ai-frameworks)<br>

## **License Agreement**
LEGAL NOTICE: By accessing, downloading or using this software and any required dependent software (the “Software Package”), you agree to the terms and conditions of the software license agreements for the Software Package, which may also include notices, disclaimers, or license terms for third party software included with the Software Package. Please refer to the [license file](https://github.com/intel-innersource/frameworks.ai.infrastructure.machine-learning-operations/blob/develop/LICENSE) for additional details.

## **Related Containers and Solutions**
[View All Containers and Solutions 🡢](https://www.intel.com/content/www/us/en/developer/tools/software-catalog/containers.html)
