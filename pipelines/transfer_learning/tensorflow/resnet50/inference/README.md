# Tensorflow ResNet50 INFERENCE - Vision Transfer Learning
## Description
This document contains instructions on how to run Vision Transfer Learning e2e pipeline with make and docker compose.
## Project Structure 
```
├── transfer-learning-inference @ v1.0.0
├── DEVCATALOG.md
├── docker-compose.yml
├── Dockerfile.vision-transfer-learning
├── Makefile
└── README.md
```
[_Makefile_](Makefile)
```
CHECKPOINT_DIR ?= /output/colorectal
DATASET_DIR ?= /data
FINAL_IMAGE_NAME ?= vision-transfer-learning
OUTPUT_DIR ?= /output
PLATFORM ?= None
PRECISION ?= FP32
SCRIPT ?= colorectal

vision-transfer-learning:
	@CHECKPOINT_DIR=${CHECKPOINT_DIR} \
	 DATASET_DIR=${DATASET_DIR} \
	 FINAL_IMAGE_NAME=${FINAL_IMAGE_NAME} \
	 OUTPUT_DIR=${OUTPUT_DIR} \
	 PLATFORM=${PLATFORM} \
	 PRECISION=${PRECISION} \
	 SCRIPT=${SCRIPT} \
	 docker compose up vision-transfer-learning --build

clean: 
	docker compose down
```
[_docker-compose.yml_](docker-compose.yml)
```
services:
  vision-transfer-learning:
    build:
      args: 
        http_proxy: ${http_proxy}
        https_proxy: ${https_proxy}
        no_proxy: ${no_proxy}
      dockerfile: Dockerfile.vision-transfer-learning
    command: conda run --no-capture-output -n transfer_learning ./${SCRIPT}.sh --inference -cp "/workspace/checkpoint"
    environment: 
      - DATASET_DIR=/workspace/data
      - OUTPUT_DIR=${OUTPUT_DIR}/${SCRIPT}
      - PLATFORM=${PLATFORM}
      - PRECISION=${PRECISION}
      - http_proxy=${http_proxy}
      - https_proxy=${https_proxy}
      - no_proxy=${no_proxy}
    image: ${FINAL_IMAGE_NAME}:inference-ubuntu-20.04
    privileged: true
    volumes: 
      - /${CHECKPOINT_DIR}:/workspace/checkpoint
      - /${DATASET_DIR}:/workspace/data
      - ${OUTPUT_DIR}:${OUTPUT_DIR}
      - ./transfer-learning-inference:/workspace/transfer-learning
    working_dir: /workspace/transfer-learning
```

# Vision Transfer Learning
End2End AI Workflow for transfer learning based image classification using ResNet50.

## Quick Start
* Pull and configure the dependent repo submodule `git submodule update --init --recursive`.

* Install [Pipeline Repository Dependencies](https://github.com/intel-innersource/frameworks.ai.infrastructure.machine-learning-operations/blob/develop/pipelines/README.md)

* Train weights using the [training version](https://github.com/intel-innersource/frameworks.ai.infrastructure.machine-learning-operations/blob/develop/pipelines/transfer_learning/tensorflow/resnet50/training). And set `CHECKPOINT_DIR` to be equal to the `${OUTPUT_DIR}/${SCRIPT}`.

* Other variables:

| Variable Name | Default | Notes |
| --- | --- | --- |
| CHECKPOINT_DIR | `/checkpoint` | Checkpoint directory, default is placeholder | 
| DATASET_DIR | `/data` | Dataset directory, optional for `SCRIPT=colorectal`, default is placeholder |
| FINAL_IMAGE_NAME | `vision-transfer-learning` | Final Docker image name |
| OUTPUT_DIR | `/output` | Output directory |
| PLATFORM | `None` | `SPR` and `None` are supported, Hyperthreaded SPR systems are not currently working |
| PRECISION | `FP32` | `bf16` and `FP32` are supported |
| SCRIPT | `colorectal` | `sports`, `resisc`, and `colorectal` are supported scripts that use different datasets/checkpoints |

## Build and Run
Build and Run with defaults:
```
make vision-transfer-learning
```
## Build and Run Example
```
$ PLATFORM=SPR make vision-transfer-learning
[+] Building 2.0s (9/9) FINISHED
 => [internal] load build definition from Dockerfile.vision-transfer-learning                                                                                                                        0.0s
 => => transferring dockerfile: 2.36kB                                                                                                                                                               0.0s
 => [internal] load .dockerignore                                                                                                                                                                    0.0s
 => => transferring context: 2B                                                                                                                                                                      0.0s
 => [internal] load metadata for docker.io/library/ubuntu:20.04                                                                                                                                      0.0s
 => [1/5] FROM docker.io/library/ubuntu:20.04                                                                                                                                                        0.0s
 => CACHED [2/5] RUN apt-get update && apt-get install --no-install-recommends --fix-missing -y     build-essential     ca-certificates     git     gcc     numactl     wget                         0.0s
 => CACHED [3/5] RUN apt-get update &&     wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh &&     bash miniconda.sh -b -p /opt/conda &&     rm m  0.0s
 => CACHED [4/5] RUN conda create -y -n transfer_learning python=3.8 &&     source activate transfer_learning &&     conda install -y -c conda-forge gperftools &&     conda install -y intel-openm  0.0s
 => [5/5] RUN mkdir -p /workspace/transfer-learning                                                                                                                                                  1.8s
 => exporting to image                                                                                                                                                                               0.0s 
 => => exporting layers                                                                                                                                                                              0.0s
 => => writing image sha256:15de220251a06ec9098c458f43c21239f1811fd5bc563bf99f322721960a717b                                                                                                         0.0s
 => => naming to docker.io/library/vision-transfer-learning:inference-23-2022-ubuntu-20.04                                                                                                           0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
[+] Running 1/0
 ⠿ Container inference-vision-transfer-learning-1  Recreated                                                                                                                                         0.1s
Attaching to inference-vision-transfer-learning-1
inference-vision-transfer-learning-1  | /usr/bin/bash: /opt/conda/envs/transfer_learning/lib/libtinfo.so.6: no version information available (required by /usr/bin/bash)
inference-vision-transfer-learning-1  | INFERENCE Default value is zero
inference-vision-transfer-learning-1  | Inference option is : 1
inference-vision-transfer-learning-1  | Checkpoint File is : /workspace/checkpoint
inference-vision-transfer-learning-1  | Platform is SPR
inference-vision-transfer-learning-1  | 2022-08-25 17:59:38.778284: I tensorflow/core/platform/cpu_feature_guard.cc:193] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX512_VNNI AVX512_BF16 AVX_VNNI AMX_TILE AMX_INT8 AMX_BF16
```
...
```
inference-vision-transfer-learning-1  | OMP: Info #255: KMP_AFFINITY: pid 22 tid 550 thread 100 bound to OS proc set 44
inference-vision-transfer-learning-1  | OMP: Info #255: KMP_AFFINITY: pid 22 tid 551 thread 101 bound to OS proc set 45
inference-vision-transfer-learning-1  | OMP: Info #255: KMP_AFFINITY: pid 22 tid 552 thread 102 bound to OS proc set 46
inference-vision-transfer-learning-1  | OMP: Info #255: KMP_AFFINITY: pid 22 tid 553 thread 103 bound to OS proc set 47
inference-vision-transfer-learning-1  | OMP: Info #255: KMP_AFFINITY: pid 22 tid 554 thread 104 bound to OS proc set 48
inference-vision-transfer-learning-1  | OMP: Info #255: KMP_AFFINITY: pid 22 tid 555 thread 105 bound to OS proc set 49
inference-vision-transfer-learning-1  | OMP: Info #255: KMP_AFFINITY: pid 22 tid 556 thread 106 bound to OS proc set 50
inference-vision-transfer-learning-1  | OMP: Info #255: KMP_AFFINITY: pid 22 tid 557 thread 107 bound to OS proc set 51
inference-vision-transfer-learning-1  | OMP: Info #255: KMP_AFFINITY: pid 22 tid 558 thread 108 bound to OS proc set 52
inference-vision-transfer-learning-1  | OMP: Info #255: KMP_AFFINITY: pid 22 tid 559 thread 109 bound to OS proc set 53
inference-vision-transfer-learning-1  | OMP: Info #255: KMP_AFFINITY: pid 22 tid 560 thread 110 bound to OS proc set 54
inference-vision-transfer-learning-1  | OMP: Info #255: KMP_AFFINITY: pid 22 tid 561 thread 111 bound to OS proc set 55
inference-vision-transfer-learning-1 exited with code 0
```

## Check Results

```
$ tail -f result.txt 
Dataset directory is  /workspace/data
Setting Output Directory
Is Tf32 enabled ? :  False
Test directory not present so using validation directory
Total classes =  8
32/32 [==============================] - 5s 127ms/step - loss: 0.2466 - acc: 0.9140
Test accuracy : 0.9139999747276306
32/32 [==============================] - 5s 137ms/step
Classification report
              precision    recall  f1-score   support

           0       0.95      0.94      0.94       112
           1       0.77      0.87      0.81       127
           2       0.86      0.74      0.80       137
           3       0.95      0.94      0.94       126
           4       0.90      0.90      0.90       126
           5       0.95      0.99      0.97       128
           6       1.00      0.96      0.98       118
           7       0.96      1.00      0.98       126

    accuracy                           0.91      1000
   macro avg       0.92      0.92      0.92      1000
weighted avg       0.92      0.91      0.91      1000

Top 1 accuracy score:  0.914
Top 5 accuracy score:  0.999
```
