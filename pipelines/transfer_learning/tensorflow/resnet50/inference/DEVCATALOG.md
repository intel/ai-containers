# **Vision Transfer Learning - Inference**

## **Description**
This guide contains instruction on how to run reference end-to-end pipeline for transfer learning with Docker container. For detailed information about the workflow, go to [End-to-End Vision Transfer Learning](https://github.com/intel/vision-based-transfer-learning-and-inference) GitHub repository.

## **Pull Docker Image**
```
docker pull intel/vision-transfer-learning:inference-ubuntu-20.04 
```

## **Download Model**
Clone [End-to-End Vision Transfer Learning](https://github.com/intel/vision-based-transfer-learning-and-inference) repository into your working directory and switch to v1.0.0 Release branch.
```
git clone https://github.com/intel/vision-based-transfer-learning-and-inference.git
git checkout v1.0.0
```

## **Download Dataset**
### Medical Imaging
Dataset is downloaded from TensorFlow website when the code is run for the first time. The dataset used for this domain is `colorectal_histology`. More details can be found at [Tensorflow Datases](https://www.tensorflow.org/datasets/catalog/colorectal_histology). 

### Remote Sensing
The dataset used for this domain is [resisc45](https://www.tensorflow.org/datasets/catalog/resisc45).  
[Download](https://onedrive.live.com/?authkey=%21AHHNaHIlzp%5FIXjs&cid=5C5E061130630A68&id=5C5E061130630A68%21107&parId=5C5E061130630A68%21112&action=locate ) the dataset and unzip the folder. The folder will later be used in `DATASET_DIR` when running the script.

## **Quick Start Scripts**
| Script Name | Description | 
| --- | --- |
| `colorectal.sh` | Script for medical imaging dataset | 
| `resisc.sh` | Script for remote sensing dataset | 

## **Customization Options**
| Script Name | Description | 
| --- | --- |
| CHECKPOINT_DIR | Train weights using the training version. Set `CHECKPOINT_DIR` to `${OUTPUT_DIR}/${SCRIPT}`. | 
| DATASET_DIR | Download the dataset the set it to `DATASET_DIR`. This directory is optional for Medical Imaging as this dataset will be downloaded from TensorFlow website when the code is run for the first time. Default to `DATASET_DIR=/data` for Medical Imaging | 
| PLATFORM | `SPR` and `None` are supported platforms | 
| PRECISION | `bf16` and `FP32 ` are supported precisions | 
| SCRIPT | `colorectal` and `resisc ` are available scripts names | 

## **Running with Docker**
The snippet below shows a quick start script running with a single instance using the following options: `PLATFORM=None`, `PRECISION=FP32` and `SCRIPT=colorectal`.
```
export OUTPUT_DIR=<directory where the output log files will be written>
export SCRIPT=colorectal
export CHECKPOINT_DIR=${OUTPUT_DIR}/${SCRIPT}
export DATASET_DIR=/data
export PLATFORM=None
export PRECISION=FP32

docker run \
  --env DATASET_DIR=${DATASET_DIR} \
  --env OUTPUT_DIR=${OUTPUT_DIR}/${SCRIPT} \
  --env PLATFORM=${PLATFORM} \
  --env PRECISION=${PRECISION} \
  --env http_proxy=${http_proxy} \
  --env https_proxy=${https_proxy} \
  --env no_proxy=${no_proxy} \
  --volume /${CHECKPOINT_DIR}:/workspace/checkpoint \
  --volume /${DATASET_DIR}:/workspace/data \
  --volume ${OUTPUT_DIR}:${OUTPUT_DIR} \
  --volume $(pwd):/workspace \
  --workdir /workspace \
  --privileged --init -it \
  intel/vision-transfer-learning:inference-ubuntu-20.04  \
  conda run --no-capture-output -n transfer_learning ./${SCRIPT}.sh --inference -cp "/workspace/checkpoint"
```
## **Documentation and Sources**

### **Get Started**
[Docker* Repository](https://hub.docker.com/u/intel) <br>
[Main GitHub*](https://github.com/intel/vision-based-transfer-learning-and-inference)<br>
[Readme](https://github.com/intel/vision-based-transfer-learning-and-inference/blob/main/README.md)<br>
[Release Notes](https://github.com/intel/vision-based-transfer-learning-and-inference/releases/tag/v1.0.0)<br>

### **Code Sources**
[Dockerfile](https://github.com/intel-innersource/frameworks.ai.infrastructure.machine-learning-operations/blob/develop/pipelines/transfer_learning/tensorflow/resnet50/inference/Dockerfile.vision-transfer-learning)<br>
[Report Issue](https://community.intel.com/t5/Intel-Optimized-AI-Frameworks/bd-p/optimized-ai-frameworks)<br>

## **License Agreement**
LEGAL NOTICE: By accessing, downloading or using this software and any required dependent software (the “Software Package”), you agree to the terms and conditions of the software license agreements for the Software Package, which may also include notices, disclaimers, or license terms for third party software included with the Software Package. Please refer to the [license file](https://github.com/intel-innersource/frameworks.ai.infrastructure.machine-learning-operations/blob/develop/LICENSE) for additional details.

## **Related Containers and Solutions**
[View All Containers and Solutions 🡢](https://www.intel.com/content/www/us/en/developer/tools/software-catalog/containers.html)
