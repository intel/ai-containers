# Tensorflow ResNet50 TRAINING - Vision Transfer Learning
## Description
This document contains instructions on how to run Vision Transfer Learning e2e pipeline with make and docker compose.
## Project Structure 
```
├── transfer-learning-training @ v1.0.0
├── DEVCATALOG.md
├── docker-compose.yml
├── Dockerfile.vision-transfer-learning
├── Makefile
└── README.md
```
[_Makefile_](Makefile)
```
DATASET_DIR ?= /data
FINAL_IMAGE_NAME ?= vision-transfer-learning
OUTPUT_DIR ?= /output
PLATFORM ?= None
PRECISION ?= FP32
SCRIPT ?= colorectal

vision-transfer-learning:
	@DATASET_DIR=${DATASET_DIR} \
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
    command: conda run --no-capture-output -n transfer_learning ./${SCRIPT}.sh
    environment: 
      - DATASET_DIR=/workspace/data
      - OUTPUT_DIR=${OUTPUT_DIR}/${SCRIPT}
      - PLATFORM=${PLATFORM}
      - PRECISION=${PRECISION}
      - http_proxy=${http_proxy}
      - https_proxy=${https_proxy}
      - no_proxy=${no_proxy}
    image: ${FINAL_IMAGE_NAME}:training-ubuntu-20.04
    privileged: true
    volumes: 
      - /${DATASET_DIR}:/workspace/data
      - ${OUTPUT_DIR}:${OUTPUT_DIR}
      - ./transfer-learning-training:/workspace/transfer-learning
    working_dir: /workspace/transfer-learning
```

# Vision Transfer Learning
End2End AI Workflow for transfer learning based image classification using ResNet50.

## Quick Start
* Pull and configure the dependent repo submodule `git submodule update --init --recursive`.

* Install [Pipeline Repository Dependencies](https://github.com/intel-innersource/frameworks.ai.infrastructure.machine-learning-operations/blob/develop/pipelines/README.md)

* Other variables:

| Variable Name | Default | Notes |
| --- | --- | --- |
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
$ DATASET_DIR=/localdisk/aia_mlops_dataset/i5-transfer-learning/sports SCRIPT=sports make vision-transfer-learning
[+] Building 0.1s (9/9) FINISHED                                                                                                                                                                          
 => [internal] load build definition from Dockerfile.vision-transfer-learning                                                                                                                        0.0s
 => => transferring dockerfile: 57B                                                                                                                                                                  0.0s
 => [internal] load .dockerignore                                                                                                                                                                    0.0s
 => => transferring context: 2B                                                                                                                                                                      0.0s
 => [internal] load metadata for docker.io/library/ubuntu:20.04                                                                                                                                      0.0s
 => [1/5] FROM docker.io/library/ubuntu:20.04                                                                                                                                                        0.0s
 => CACHED [2/5] RUN apt-get update && apt-get install --no-install-recommends --fix-missing -y     build-essential     ca-certificates     git     gcc     numactl     wget                         0.0s
 => CACHED [3/5] RUN apt-get update &&     wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh &&     bash miniconda.sh -b -p /opt/conda &&     rm m  0.0s
 => CACHED [4/5] RUN conda create -y -n transfer_learning python=3.8 &&     source activate transfer_learning &&     conda install -y -c conda-forge gperftools &&     conda install -y intel-openm  0.0s
 => CACHED [5/5] RUN mkdir -p /workspace/transfer-learning                                                                                                                                           0.0s
 => exporting to image                                                                                                                                                                               0.0s
 => => exporting layers                                                                                                                                                                              0.0s
 => => writing image sha256:20fc21d79272d6af76735b20eb456bcf1a19019e8541e658292d3be60cb5b80f                                                                                                         0.0s
 => => naming to docker.io/library/vision-transfer-learning:training-ww23-2022-ubuntu-20.04                                                                                                          0.0s
WARN[0000] Found orphan containers ([hadoop-main]) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up. 
[+] Running 1/1
 ⠿ Container training-vision-transfer-learning-1  Recreated                                                                                                                                          0.1s
Attaching to training-vision-transfer-learning-1
training-vision-transfer-learning-1  | /usr/bin/bash: /opt/conda/envs/transfer_learning/lib/libtinfo.so.6: no version information available (required by /usr/bin/bash)
training-vision-transfer-learning-1  | INFERENCE Default value is zero
training-vision-transfer-learning-1  | WARNING:tensorflow:Please fix your imports. Module tensorflow.python.training.tracking.base has been moved to tensorflow.python.trackable.base. The old module will be deleted in version 2.11.
training-vision-transfer-learning-1  | WARNING:tensorflow:Please fix your imports. Module tensorflow.python.training.checkpoint_management has been moved to tensorflow.python.checkpoint.checkpoint_management. The old module will be deleted in version 2.9.
training-vision-transfer-learning-1  | WARNING:tensorflow:Please fix your imports. Module tensorflow.python.training.tracking.resource has been moved to tensorflow.python.trackable.resource. The old module will be deleted in version 2.11.
training-vision-transfer-learning-1  | WARNING:tensorflow:Please fix your imports. Module tensorflow.python.training.tracking.util has been moved to tensorflow.python.checkpoint.checkpoint. The old module will be deleted in version 2.11.
training-vision-transfer-learning-1  | WARNING:tensorflow:Please fix your imports. Module tensorflow.python.training.tracking.base_delegate has been moved to tensorflow.python.trackable.base_delegate. The old module will be deleted in version 2.11.
training-vision-transfer-learning-1  | WARNING:tensorflow:Please fix your imports. Module tensorflow.python.training.tracking.graph_view has been moved to tensorflow.python.checkpoint.graph_view. The old module will be deleted in version 2.11.
training-vision-transfer-learning-1  | WARNING:tensorflow:Please fix your imports. Module tensorflow.python.training.tracking.python_state has been moved to tensorflow.python.trackable.python_state. The old module will be deleted in version 2.11.
training-vision-transfer-learning-1  | WARNING:tensorflow:Please fix your imports. Module tensorflow.python.training.saving.functional_saver has been moved to tensorflow.python.checkpoint.functional_saver. The old module will be deleted in version 2.11.
training-vision-transfer-learning-1  | WARNING:tensorflow:Please fix your imports. Module tensorflow.python.training.saving.checkpoint_options has been moved to tensorflow.python.checkpoint.checkpoint_options. The old module will be deleted in version 2.11.
training-vision-transfer-learning-1  | 2022-08-30 16:18:31.273775: I tensorflow/core/common_runtime/process_util.cc:146] Creating new thread pool with default inter op setting: 2. Tune using inter_op_parallelism_threads for best performance.
training-vision-transfer-learning-1 exited with code 0
```

## Check Results

```
$ tail -f /output/sports/result.txt 
Dataset directory is  /workspace/data
Setting Output Directory
Is Tf32 enabled ? :  False
Found 3752 files belonging to 2 classes.
Found 804 files belonging to 2 classes.
Found 805 files belonging to 2 classes.
Total classes =  2
Epoch 1/200
118/118 [==============================] - 62s 500ms/step - loss: 0.2118 - acc: 0.9166 - val_loss: 0.0951 - val_acc: 0.9664 - lr: 0.0010
Epoch 2/200
118/118 [==============================] - 49s 410ms/step - loss: 0.0696 - acc: 0.9827 - val_loss: 0.0608 - val_acc: 0.9813 - lr: 0.0010
Epoch 3/200
118/118 [==============================] - 48s 401ms/step - loss: 0.0461 - acc: 0.9901 - val_loss: 0.0484 - val_acc: 0.9863 - lr: 0.0010
Epoch 4/200
118/118 [==============================] - 42s 355ms/step - loss: 0.0353 - acc: 0.9917 - val_loss: 0.0440 - val_acc: 0.9863 - lr: 0.0010
Epoch 5/200
118/118 [==============================] - 42s 353ms/step - loss: 0.0281 - acc: 0.9955 - val_loss: 0.0395 - val_acc: 0.9851 - lr: 0.0010
Epoch 6/200
118/118 [==============================] - 50s 422ms/step - loss: 0.0227 - acc: 0.9963 - val_loss: 0.0345 - val_acc: 0.9876 - lr: 0.0010
Epoch 7/200
118/118 [==============================] - 48s 403ms/step - loss: 0.0185 - acc: 0.9976 - val_loss: 0.0307 - val_acc: 0.9900 - lr: 0.0010
Epoch 8/200
118/118 [==============================] - 45s 377ms/step - loss: 0.0149 - acc: 0.9984 - val_loss: 0.0317 - val_acc: 0.9888 - lr: 0.0010
Epoch 9/200
118/118 [==============================] - 51s 433ms/step - loss: 0.0127 - acc: 0.9984 - val_loss: 0.0257 - val_acc: 0.9950 - lr: 0.0010
Epoch 10/200
118/118 [==============================] - 43s 360ms/step - loss: 0.0109 - acc: 0.9995 - val_loss: 0.0243 - val_acc: 0.9938 - lr: 0.0010
Epoch 11/200
118/118 [==============================] - 46s 384ms/step - loss: 0.0101 - acc: 1.0000 - val_loss: 0.0249 - val_acc: 0.9900 - lr: 0.0010
Epoch 12/200
118/118 [==============================] - 43s 362ms/step - loss: 0.0083 - acc: 0.9997 - val_loss: 0.0221 - val_acc: 0.9950 - lr: 0.0010
Epoch 13/200
118/118 [==============================] - 43s 366ms/step - loss: 0.0071 - acc: 1.0000 - val_loss: 0.0217 - val_acc: 0.9950 - lr: 0.0010
Epoch 14/200
118/118 [==============================] - 43s 358ms/step - loss: 0.0063 - acc: 1.0000 - val_loss: 0.0223 - val_acc: 0.9913 - lr: 0.0010
Epoch 15/200
118/118 [==============================] - 44s 375ms/step - loss: 0.0061 - acc: 1.0000 - val_loss: 0.0231 - val_acc: 0.9913 - lr: 0.0010
Epoch 16/200
118/118 [==============================] - 43s 362ms/step - loss: 0.0051 - acc: 1.0000 - val_loss: 0.0207 - val_acc: 0.9913 - lr: 0.0010
Epoch 17/200
118/118 [==============================] - 44s 369ms/step - loss: 0.0047 - acc: 1.0000 - val_loss: 0.0198 - val_acc: 0.9925 - lr: 0.0010
Epoch 18/200
118/118 [==============================] - 43s 362ms/step - loss: 0.0042 - acc: 1.0000 - val_loss: 0.0205 - val_acc: 0.9913 - lr: 0.0010
Epoch 19/200
118/118 [==============================] - 43s 363ms/step - loss: 0.0038 - acc: 1.0000 - val_loss: 0.0196 - val_acc: 0.9913 - lr: 0.0010
Epoch 20/200
118/118 [==============================] - 44s 368ms/step - loss: 0.0034 - acc: 1.0000 - val_loss: 0.0198 - val_acc: 0.9913 - lr: 0.0010
Epoch 21/200
118/118 [==============================] - 43s 361ms/step - loss: 0.0032 - acc: 1.0000 - val_loss: 0.0231 - val_acc: 0.9913 - lr: 0.0010
Epoch 22/200
118/118 [==============================] - 44s 375ms/step - loss: 0.0029 - acc: 1.0000 - val_loss: 0.0188 - val_acc: 0.9938 - lr: 0.0010
Epoch 23/200
118/118 [==============================] - 43s 359ms/step - loss: 0.0027 - acc: 1.0000 - val_loss: 0.0193 - val_acc: 0.9913 - lr: 0.0010
Epoch 24/200
118/118 [==============================] - 44s 368ms/step - loss: 0.0024 - acc: 1.0000 - val_loss: 0.0184 - val_acc: 0.9925 - lr: 0.0010
Epoch 25/200
118/118 [==============================] - 42s 355ms/step - loss: 0.0023 - acc: 1.0000 - val_loss: 0.0197 - val_acc: 0.9913 - lr: 0.0010
Epoch 26/200
118/118 [==============================] - 44s 374ms/step - loss: 0.0021 - acc: 1.0000 - val_loss: 0.0200 - val_acc: 0.9913 - lr: 0.0010
Epoch 27/200
118/118 [==============================] - 44s 368ms/step - loss: 0.0020 - acc: 1.0000 - val_loss: 0.0202 - val_acc: 0.9913 - lr: 0.0010
Epoch 28/200
118/118 [==============================] - 44s 372ms/step - loss: 0.0018 - acc: 1.0000 - val_loss: 0.0173 - val_acc: 0.9938 - lr: 0.0010
Epoch 29/200
118/118 [==============================] - 47s 396ms/step - loss: 0.0018 - acc: 1.0000 - val_loss: 0.0188 - val_acc: 0.9925 - lr: 0.0010
Epoch 30/200
118/118 [==============================] - 43s 365ms/step - loss: 0.0016 - acc: 1.0000 - val_loss: 0.0185 - val_acc: 0.9925 - lr: 0.0010
Epoch 31/200
118/118 [==============================] - 45s 376ms/step - loss: 0.0015 - acc: 1.0000 - val_loss: 0.0179 - val_acc: 0.9925 - lr: 0.0010
Epoch 32/200
118/118 [==============================] - 44s 367ms/step - loss: 0.0014 - acc: 1.0000 - val_loss: 0.0183 - val_acc: 0.9925 - lr: 0.0010
Epoch 33/200
118/118 [==============================] - ETA: 0s - loss: 0.0013 - acc: 1.0000     
Epoch 33: ReduceLROnPlateau reducing learning rate to 0.00020000000949949026.
118/118 [==============================] - 47s 393ms/step - loss: 0.0013 - acc: 1.0000 - val_loss: 0.0180 - val_acc: 0.9925 - lr: 0.0010
Epoch 34/200
118/118 [==============================] - 43s 365ms/step - loss: 0.0011 - acc: 1.0000 - val_loss: 0.0185 - val_acc: 0.9925 - lr: 2.0000e-04
Epoch 35/200
118/118 [==============================] - 52s 442ms/step - loss: 0.0011 - acc: 1.0000 - val_loss: 0.0192 - val_acc: 0.9925 - lr: 2.0000e-04
Epoch 36/200
118/118 [==============================] - 46s 384ms/step - loss: 0.0011 - acc: 1.0000 - val_loss: 0.0182 - val_acc: 0.9925 - lr: 2.0000e-04
Epoch 37/200
118/118 [==============================] - 51s 428ms/step - loss: 0.0011 - acc: 1.0000 - val_loss: 0.0202 - val_acc: 0.9913 - lr: 2.0000e-04
Epoch 38/200
118/118 [==============================] - ETA: 0s - loss: 0.0011 - acc: 1.0000     
Epoch 38: ReduceLROnPlateau reducing learning rate to 4.0000001899898055e-05.
118/118 [==============================] - 57s 483ms/step - loss: 0.0011 - acc: 1.0000 - val_loss: 0.0184 - val_acc: 0.9925 - lr: 2.0000e-04
Total elapsed time =  2522.6976577951573
Maximum validation accuracy =  0.9950248599052429
26/26 [==============================] - 10s 350ms/step - loss: 0.0255 - acc: 0.9901
Test accuracy : 0.9900621175765991
26/26 [==============================] - 12s 424ms/step
Classification report
              precision    recall  f1-score   support

           0       1.00      0.99      0.99       450
           1       0.98      0.99      0.99       355

    accuracy                           0.99       805
   macro avg       0.99      0.99      0.99       805
weighted avg       0.99      0.99      0.99       805
```
