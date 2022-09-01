# PyTorch BERT Large TRAINING - Hugging Face DLSA
## Description
This document contains instructions on how to run hugging face DLSA e2e pipelines with make and docker compose.
## Project Structure 
```
├── dlsa @ dlsa_multinode_ipex_v1.2
├── docker-compose.yml
├── Dockerfile.hugging-face-dlsa
├── Makefile
└── README.md
```
[_Makefile_](Makefile)
```
DATASET ?= sst2
DATASET_DIR ?= /data
FINAL_IMAGE_NAME ?= hugging-face-dlsa
MODEL ?= bert-large-uncased
OUTPUT_DIR ?= /output

hugging-face-dlsa:
	mkdir ./dlsa/profiling-transformers/datasets && cp -r ${DATASET_DIR} ./dlsa/profiling-transformers/datasets
	@DATASET=${DATASET} \
	 FINAL_IMAGE_NAME=${FINAL_IMAGE_NAME} \
	 MODEL=${MODEL} \
	 OUTPUT_DIR=${OUTPUT_DIR} \
 	 docker compose up hugging-face-dlsa --build

clean: 
	rm -rf ./dlsa/profiling-transformers/datasets
	docker compose down
```
[_docker-compose.yml_](docker-compose.yml)
```
services:
  hugging-face-dlsa:
    build:
      args: 
        http_proxy: ${http_proxy}
        https_proxy: ${https_proxy}
        no_proxy: ${no_proxy}
      dockerfile: Dockerfile.hugging-face-dlsa
    command: /workspace/dlsa/profiling-transformers/run_dist.sh -np 1 -ppn 1 /workspace/dlsa/profiling-transformers/run_ipex_native.sh
    environment: 
      - DATASET=${DATASET}
      - MODEL_NAME_OR_PATH=${MODEL}
      - OUTPUT_DIR=${OUTPUT_DIR}/fine_tuned
      - http_proxy=${http_proxy}
      - https_proxy=${https_proxy}
      - no_proxy=${no_proxy}
    image: ${FINAL_IMAGE_NAME}:training-intel-optimized-pytorch-latest
    privileged: true
    volumes: 
      - ${OUTPUT_DIR}:${OUTPUT_DIR}
      - ./dlsa:/workspace/dlsa
    working_dir: /workspace/dlsa/profiling-transformers
```

# Hugging Face DLSA
End2End AI Workflow utilizing Hugging Face for Document-Level Sentiment Analysis

## Quick Start
* Pull and configure the dependent repo submodule `git submodule update --init --recursive`.

* Install [Pipeline Repository Dependencies](https://github.com/intel-innersource/frameworks.ai.infrastructure.machine-learning-operations/blob/develop/pipelines/README.md)

* Other variables:

| Variable Name | Default | Notes |
| --- | --- | --- |
| DATASET | `sst2` | Name of dataset, `sst2` and `imdb` are supported |
| DATASET_DIR | `/data` | DLSA dataset directory, default is placeholder, `aclImdb` is for `DATASET=imdb` and `sst` is for `DATASET=sst2` |
| FINAL_IMAGE_NAME | `hugging-face-dlsa` | Final Docker image name |
| MODEL | `bert-large-uncased` | Name of model on [Huggingface](https://huggingface.co). |
| OUTPUT_DIR | `/output` | Output directory |
## Build and Run
Build and Run with defaults:
```
$ DATASET_DIR=/localdisk/aia_mlops_dataset/t2-hugging-face-dlsa/sst make hugging-face-dlsa
```
## Build and Run Example
```
$ make hugging-face-dlsa
[+] Building 97.7s (9/9) FINISHED                                                                                                                                                                                          
 => [internal] load build definition from Dockerfile.hugging-face-dlsa                                                                                                                                                0.0s
 => => transferring dockerfile: 1.05kB                                                                                                                                                                                0.0s
 => [internal] load .dockerignore                                                                                                                                                                                     0.0s
 => => transferring context: 2B                                                                                                                                                                                       0.0s
 => [internal] load metadata for docker.io/intel/intel-optimized-pytorch:latest                                                                                                                                       1.2s
 => [auth] intel/intel-optimized-pytorch:pull token for registry-1.docker.io                                                                                                                                          0.0s
 => [1/4] FROM docker.io/intel/intel-optimized-pytorch:latest@sha256:37fd3ab2e8e40272780aeeb99631e9168f0cbecf38c397bda584ca7ec645e359                                                                                33.7s
 => => resolve docker.io/intel/intel-optimized-pytorch:latest@sha256:37fd3ab2e8e40272780aeeb99631e9168f0cbecf38c397bda584ca7ec645e359                                                                                 0.0s
 => => sha256:95e46843f5d3a46cc9eeb35c27d6f0f58d75f4d7f7fd0f463c6c5ff75918aee0 4.00kB / 4.00kB                                                                                                                        0.0s
 => => sha256:4f419499a9a5bad041fbf20b19ebf7aa21b343d62665947f9be58f2ca9019d65 184B / 184B                                                                                                                            0.2s
 => => sha256:37fd3ab2e8e40272780aeeb99631e9168f0cbecf38c397bda584ca7ec645e359 1.78kB / 1.78kB                                                                                                                        0.0s
 => => sha256:8e5c1b329fe39c318c0d49821b339fb94a215c5dc0a2898c8030b5a4d091bcba 28.57MB / 28.57MB                                                                                                                      0.7s
 => => sha256:7acca15cf7e304377750d2d34d63130f7af645384659f6502b27eef5da37a048 145.31MB / 145.31MB                                                                                                                    4.9s
 => => sha256:d25748f32da6f2ed3e3ed10d063ee06df0b25a594081fe9caeec13ee3ce58516 256B / 256B                                                                                                                            0.5s
 => => sha256:9a9f79fe09de72088aba7c5d904807b40af2f4078a17aa589bcbf4654b0adad2 705.19MB / 705.19MB                                                                                                                   19.4s
 => => sha256:4507af6d9549d9ba35b46f19157ff5591f0d16f2fb18f760a0d122f0641b940d 192B / 192B                                                                                                                            0.9s
 => => extracting sha256:8e5c1b329fe39c318c0d49821b339fb94a215c5dc0a2898c8030b5a4d091bcba                                                                                                                             0.5s
 => => sha256:08036a96427d59e64f289f6d420a8a056ea1a3d419985e8e8aa2bb8c5e014c88 62.13kB / 62.13kB                                                                                                                      1.2s
 => => extracting sha256:7acca15cf7e304377750d2d34d63130f7af645384659f6502b27eef5da37a048                                                                                                                             2.9s
 => => extracting sha256:4f419499a9a5bad041fbf20b19ebf7aa21b343d62665947f9be58f2ca9019d65                                                                                                                             0.0s
 => => extracting sha256:d25748f32da6f2ed3e3ed10d063ee06df0b25a594081fe9caeec13ee3ce58516                                                                                                                             0.0s
 => => extracting sha256:9a9f79fe09de72088aba7c5d904807b40af2f4078a17aa589bcbf4654b0adad2                                                                                                                            13.3s
 => => extracting sha256:4507af6d9549d9ba35b46f19157ff5591f0d16f2fb18f760a0d122f0641b940d                                                                                                                             0.0s
 => => extracting sha256:08036a96427d59e64f289f6d420a8a056ea1a3d419985e8e8aa2bb8c5e014c88                                                                                                                             0.0s
 => [2/4] RUN apt-get update && apt-get install --no-install-recommends --fix-missing -y     ca-certificates     git     libgomp1     numactl     patch     wget     mpich                                           22.6s
 => [3/4] RUN mkdir -p /workspace                                                                                                                                                                                     0.6s
 => [4/4] RUN pip install --upgrade pip &&     pip install astunparse                 cffi                 cmake                 dataclasses                 datasets==2.3.2                 intel-openmp            33.6s 
 => exporting to image                                                                                                                                                                                                5.9s 
 => => exporting layers                                                                                                                                                                                               5.9s 
 => => writing image sha256:87b75ae09f3b6ac3f04b245c0aaa0288f9064593fcffb57f9389bf6e59a82f30                                                                                                                          0.0s 
 => => naming to docker.io/library/hugging-face-dlsa:training-intel-optimized-pytorch-latest                                                                                                                          0.0s 
WARN[0097] Found orphan containers ([training-vision-transfer-learning-1]) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up.                                                                                                                                                                                                                     
[+] Running 1/1
 ⠿ Container training-hugging-face-dlsa-1  Created                                                                                                                                                                    0.2s
Attaching to training-hugging-face-dlsa-1
training-hugging-face-dlsa-1  | Running 2 tasks on 1 nodes with ppn=2
training-hugging-face-dlsa-1  | /opt/conda/bin/python
training-hugging-face-dlsa-1  | /usr/bin/gcc
training-hugging-face-dlsa-1  | /usr/bin/mpicc
training-hugging-face-dlsa-1  | /usr/bin/mpiexec.hydra
training-hugging-face-dlsa-1  | #### INITIAL ENV ####
training-hugging-face-dlsa-1  | Using CCL_WORKER_AFFINITY=0,28
training-hugging-face-dlsa-1  | Using CCL_WORKER_COUNT=1
training-hugging-face-dlsa-1  | Using I_MPI_PIN_DOMAIN=[0xFFFFFFE,0xFFFFFFE0000000]
training-hugging-face-dlsa-1  | Using KMP_BLOCKTIME=1
training-hugging-face-dlsa-1  | Using KMP_HW_SUBSET=1T
training-hugging-face-dlsa-1  | Using OMP_NUM_THREADS=27
training-hugging-face-dlsa-1  | Using LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so:/usr/lib/x86_64-linux-gnu/libtcmalloc.so:/opt/conda/lib/libiomp5.so:
training-hugging-face-dlsa-1  | Using PYTORCH_MPI_THREAD_AFFINITY=0,28
training-hugging-face-dlsa-1  | Using DATALOADER_WORKER_COUNT=0
training-hugging-face-dlsa-1  | Using ARGS_NTASKS=2
training-hugging-face-dlsa-1  | Using ARGS_PPN=2
training-hugging-face-dlsa-1  | #### INITIAL ENV ####
training-hugging-face-dlsa-1  | PyTorch version: 1.11.0+cpu
training-hugging-face-dlsa-1  | MASTER_ADDR=e7930b8a9eae
training-hugging-face-dlsa-1  | [0] e7930b8a9eae
training-hugging-face-dlsa-1  | [1] e7930b8a9eae
```
...
```
training-hugging-face-dlsa-1  | [0] *********** TEST_METRICS ***********
training-hugging-face-dlsa-1  | [0] Accuracy: 0.5091743119266054
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] 'Inference' took 66.178s (66,177,509,482ns)
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] ##############################
training-hugging-face-dlsa-1  | [0] Benchmark Summary:
training-hugging-face-dlsa-1  | [0] ##############################
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] 'Load Data' took 0.064s (63,980,232ns)
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] '----Training data encoding' took 1.625s (1,625,314,718ns)
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] '----Training tensor data convert' took 0.000s (86,070ns)
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] '----PyTorch test data encoding' took 0.030s (30,427,632ns)
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] '----PyTorch test tensor data convert' took 0.000s (69,433ns)
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] '----Init tokenizer' took 6.438s (6,438,305,050ns)
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] 'Pre-process' took 6.438s (6,438,316,023ns)
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] 'Load Model' took 25.581s (25,581,075,968ns)
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] 'Process int8 model' took 0.000s (1,322ns)
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] 'Process bf16 model' took 0.000s (755ns)
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] '--------Init Fine-Tuning' took 0.007s (7,005,553ns)
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] '--------Training Loop' took 6400.528s (6,400,528,084,071ns)
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] '--------Save Fine-Tuned Model' took 1.846s (1,845,884,212ns)
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] 'Fine-Tune' took 6402.381s (6,402,381,151,290ns)
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] 'Inference' took 66.178s (66,177,509,482ns)
training-hugging-face-dlsa-1  | [0] **********************************************************************
training-hugging-face-dlsa-1  | [0] 
training-hugging-face-dlsa-1  | [0] 
Train Step: 100%|██████████| 2105/2105 [1:48:26<00:00,  3.09s/it][1] [1] 
Epoch: 100%|██████████| 1/1 [1:48:26<00:00, 6506.01s/it][1] s/it][1] 
Test Step:   0%|          | 0/109 [00:00<?, ?it/s][1] 
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] '--------Training Loop' took 6506.010s (6,506,009,911,526ns)
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] '--------Save Fine-Tuned Model' took 5.175s (5,175,177,382ns)
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 'Fine-Tune' took 6511.189s (6,511,189,374,535ns)
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 
Test Step: 100%|██████████| 109/109 [01:08<00:00,  1.58it/s][1] 
training-hugging-face-dlsa-1  | [1] *********** TEST_METRICS ***********
training-hugging-face-dlsa-1  | [1] Accuracy: 0.5091743119266054
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 'Inference' took 68.940s (68,939,695,151ns)
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] ##############################
training-hugging-face-dlsa-1  | [1] Benchmark Summary:
training-hugging-face-dlsa-1  | [1] ##############################
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 'Load Data' took 0.061s (60,809,048ns)
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] '----Training data encoding' took 1.639s (1,638,570,780ns)
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] '----Training tensor data convert' took 0.000s (74,039ns)
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] '----PyTorch test data encoding' took 0.035s (35,348,035ns)
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] '----PyTorch test tensor data convert' took 0.000s (62,836ns)
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] '----Init tokenizer' took 6.566s (6,566,305,202ns)
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 'Pre-process' took 6.566s (6,566,314,800ns)
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 'Load Model' took 25.585s (25,584,507,153ns)
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 'Process int8 model' took 0.000s (1,046ns)
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 'Process bf16 model' took 0.000s (1,156ns)
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] '--------Init Fine-Tuning' took 0.004s (4,075,527ns)
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] '--------Training Loop' took 6506.010s (6,506,009,911,526ns)
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] '--------Save Fine-Tuned Model' took 5.175s (5,175,177,382ns)
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 'Fine-Tune' took 6511.189s (6,511,189,374,535ns)
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 'Inference' took 68.940s (68,939,695,151ns)
training-hugging-face-dlsa-1  | [1] **********************************************************************
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | [1] 
training-hugging-face-dlsa-1  | End Time:    Wed Aug 31 17:40:30 UTC 2022
training-hugging-face-dlsa-1  | Total Time: 110 min and 14 sec
training-hugging-face-dlsa-1 exited with code 0
```
