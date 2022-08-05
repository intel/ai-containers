# PyTorch BERT Large TRAINING - Hugging Face DLSA
## Description
This document contains instructions on how to run hugging face DLSA e2e pipelines with make and docker compose.
## Project Structure 
```
├── dlsa @ dlsa_multinode_ddp
├── docker-compose.yml
├── Dockerfile.hugging-face-dlsa-public
├── Dockerfile.hugging-face-dlsa-weekly
├── Makefile
└── README.md
```
[_Makefile_](Makefile)
```
DATASET ?= sst2
FINAL_IMAGE_NAME ?= hugging-face-dlsa
MODEL ?= bert-large-cased
OUTPUT_DIR ?= /output
RELEASE ?= weekly
# Weekly Envs
WHL_WW ?= $$(date +%V)
WHL_YR ?= $$(date +%Y)

hugging-face-dlsa:
	@DATASET=${DATASET} \
	 FINAL_IMAGE_NAME=${FINAL_IMAGE_NAME} \
	 MODEL=${MODEL} \
	 OUTPUT_DIR=${OUTPUT_DIR} \
	 RELEASE=${RELEASE} \
	 WHL_WW=${WHL_WW} \
	 WHL_YR=${WHL_YR} \
 	 docker compose up hugging-face-dlsa-${RELEASE} --build

clean: 
	docker compose down
```
[_docker-compose.yml_](docker-compose.yml)
```
services:
  hugging-face-dlsa-public:
    build:
      args: 
        http_proxy: ${http_proxy}
        https_proxy: ${https_proxy}
        no_proxy: ${no_proxy}
      dockerfile: Dockerfile.hugging-face-dlsa-public
    command: /workspace/dlsa/profiling-transformers/run_dist.sh -np 1 -ppn 1 /workspace/dlsa/profiling-transformers/run_pt_trainer.sh
    environment: 
      - DATASET=${DATASET}
      - MODEL=${MODEL}
      - OUTPUT_DIR=${OUTPUT_DIR}/fine_tuned
      - http_proxy=${http_proxy}
      - https_proxy=${https_proxy}
      - no_proxy=${no_proxy}
    image: ${FINAL_IMAGE_NAME}:training-public-intel-optimized-pytorch-latest
    privileged: true
    volumes: 
      - ${OUTPUT_DIR}:${OUTPUT_DIR}
      - ./dlsa:/workspace/dlsa
    working_dir: /workspace/dlsa/profiling-transformers
  hugging-face-dlsa-weekly:
    build:
      args: 
        WHL_WW: ${WHL_WW}
        WHL_YR: ${WHL_YR}
        http_proxy: ${http_proxy}
        https_proxy: ${https_proxy}
        no_proxy: ${no_proxy}
      dockerfile: Dockerfile.hugging-face-dlsa-${RELEASE}
    command: /workspace/dlsa/profiling-transformers/run_dist.sh -np 1 -ppn 1 /workspace/dlsa/profiling-transformers/run_pt_trainer.sh
    environment: 
      - DATASET=${DATASET}
      - MODEL=${MODEL}
      - OUTPUT_DIR=${OUTPUT_DIR}/fine_tuned
      - http_proxy=${http_proxy}
      - https_proxy=${https_proxy}
      - no_proxy=${no_proxy}
    image: ${FINAL_IMAGE_NAME}:training-weekly-ww${WHL_WW}-${WHL_YR}-ubuntu-20.04
    privileged: true
    volumes: 
      - ${OUTPUT_DIR}:${OUTPUT_DIR}
      - ./dlsa:/workspace/dlsa
    working_dir: /workspace/dlsa/profiling-transformers
```

# Hugging Face DLSA
End2End AI Workflow utilizing Hugging Face. More information [here](https://cautious-succotash-7ed62415.pages.github.io/)

## Quick Start
* Pull and configure the dependent repo submodule `git submodule update --init --recursive`.

* Other variables:

| Variable Name | Default | Notes |
| --- | --- | --- |
| FINAL_IMAGE_NAME | `hugging-face-dlsa` | Final Docker image name |
| MODEL | `bert-large-cased` | Name of model on [Huggingface](https://huggingface.co). |
| OUTPUT_DIR | `/output` | Output directory |
| RELEASE | `weekly` | Container type. Either `public` or `weekly` |
| WHL_WW | Current work week | Set to latest by default. Required when `RELEASE=weekly` |
| WHL_YR | Current year | Set to latest by default. Required when `RELEASE=weekly` |
## Build and Run
Build and Run with defaults:
```
make hugging-face-dlsa
```
## Build and Run Example
```
$ RELEASE=weekly make hugging-face-dlsa
[+] Building 0.4s (10/10) FINISHED                                                                       
 => [internal] load build definition from Dockerfile.hugging-face-dlsa-weekly                       0.0s
 => => transferring dockerfile: 57B                                                                 0.0s
 => [internal] load .dockerignore                                                                   0.0s
 => => transferring context: 2B                                                                     0.0s
 => [internal] load metadata for docker.io/library/ubuntu:20.04                                     0.4s
 => [1/6] FROM docker.io/library/ubuntu:20.04@sha256:fd92c36d3cb9b1d027c4d2a72c6bf0125da82425fc2ca  0.0s
 => CACHED [2/6] RUN apt-get update && apt-get install --no-install-recommends --fix-missing -y     0.0s
 => CACHED [3/6] RUN apt-get update &&     wget --quiet https://repo.anaconda.com/miniconda/Minico  0.0s
 => CACHED [4/6] RUN conda create -yn dlsa python=3.7 &&     source activate dlsa &&     conda ins  0.0s
 => CACHED [5/6] RUN mkdir -p /workspace                                                            0.0s
 => CACHED [6/6] RUN export PATH=/opt/conda/envs/dlsa/bin:/opt/conda/bin:/usr/local/sbin:/usr/loca  0.0s
 => exporting to image                                                                              0.0s
 => => exporting layers                                                                             0.0s
 => => writing image sha256:9c3105cf758eb1b1dfe596f5a52430ecbeb420290ea2a77069d838110f68aa92        0.0s
 => => naming to docker.io/library/hugging-face-dlsa:training-weekly-ww30-2022-ubuntu-20.04         0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
[+] Running 1/0
 ⠿ Container training-hugging-face-dlsa-weekly-1  Created                                           0.0s
Attaching to training-hugging-face-dlsa-weekly-1
training-hugging-face-dlsa-weekly-1  | Running 1 tasks on 1 nodes with ppn=1
training-hugging-face-dlsa-weekly-1  | /opt/conda/bin/python
training-hugging-face-dlsa-weekly-1  | /usr/bin/mpicc
training-hugging-face-dlsa-weekly-1  | /usr/bin/mpiexec.hydra
training-hugging-face-dlsa-weekly-1  | #### INITIAL ENV ####
training-hugging-face-dlsa-weekly-1  | Using CCL_WORKER_COUNT=0
training-hugging-face-dlsa-weekly-1  | Using I_MPI_PIN_DOMAIN=[0xFFFFFFFFFF]
training-hugging-face-dlsa-weekly-1  | Using OMP_NUM_THREADS=40
training-hugging-face-dlsa-weekly-1  | Using PYTORCH_MPI_THREAD_AFFINITY=0
training-hugging-face-dlsa-weekly-1  | Using DATALOADER_WORKER_COUNT=0
training-hugging-face-dlsa-weekly-1  | Using ARGS_NTASKS=1
training-hugging-face-dlsa-weekly-1  | Using ARGS_PPN=1
training-hugging-face-dlsa-weekly-1  | #### INITIAL ENV ####
training-hugging-face-dlsa-weekly-1  | PyTorch version: 
training-hugging-face-dlsa-weekly-1  | MASTER_ADDR=b87e272340b1
training-hugging-face-dlsa-weekly-1  | [0] b87e272340b1
training-hugging-face-dlsa-weekly-1  | Running mpiexec.hydra -np 1 -ppn 1 -l -genv I_MPI_PIN_DOMAIN=[0xFFFFFFFFFF] -genv CCL_WORKER_AFFINITY= -genv CCL_WORKER_COUNT=0 -genv OMP_NUM_THREADS=40 /workspace/dlsa/profiling-transformers/run_pt_trainer.sh
training-hugging-face-dlsa-weekly-1  | Start Time:  Wed Jul 27 20:10:29 UTC 2022
training-hugging-face-dlsa-weekly-1  | [0] PyTorch: setting up devices
training-hugging-face-dlsa-weekly-1  | [0] The default value for the training argument `--report_to` will change in v5 (from all installed integrations to none). In v5, you will need to use `--report_to all` to get the same behavior as now. You should start updating your code and make this info disappear :-).
training-hugging-face-dlsa-weekly-1  | [0] Downloading and preparing dataset glue/sst2 (download: 7.09 MiB, generated: 4.81 MiB, post-processed: Unknown size, total: 11.90 MiB) to /root/.cache/huggingface/datasets/glue/sst2/1.0.0/dacbe3125aa31d7f70367a07a8a9e72a5a0bfeb5fc42e75c9db75b96da6053ad...
Downloading: 100%|██████████| 7.44M/7.44M [00:00<00:00, 69.2MB/s][0] 
                                [0] Dataset glue downloaded and prepared to /root/.cache/huggingface/datasets/glue/sst2/1.0.0/dacbe3125aa31d7f70367a07a8a9e72a5a0bfeb5fc42e75c9db75b96da6053ad. Subsequent calls will reuse this data.
100%|██████████| 3/3 [00:00<00:00, 1138.11it/s][0] 
training-hugging-face-dlsa-weekly-1  | [0] https://huggingface.co/bert-large-uncased/resolve/main/tokenizer_config.json not found in cache or force_download set to True, downloading to /root/.cache/huggingface/transformers/tmpsm8ghgpi
training-hugging-face-dlsa-weekly-1  | [0] 
training-hugging-face-dlsa-weekly-1  | [0] **********************************************************************
training-hugging-face-dlsa-weekly-1  | [0] 'Load Data' took 2.410s (2,409,555,592ns)
training-hugging-face-dlsa-weekly-1  | [0] **********************************************************************
```
...
```
training-hugging-face-dlsa-weekly-1  | [0] ##############################
training-hugging-face-dlsa-weekly-1  | [0] Benchmark Summary:
training-hugging-face-dlsa-weekly-1  | [0] ##############################
training-hugging-face-dlsa-weekly-1  | [0] 
training-hugging-face-dlsa-weekly-1  | [0] 
training-hugging-face-dlsa-weekly-1  | [0] **********************************************************************
training-hugging-face-dlsa-weekly-1  | [0] 'Load Data' took 2.410s (2,409,555,592ns)
training-hugging-face-dlsa-weekly-1  | [0] **********************************************************************
training-hugging-face-dlsa-weekly-1  | [0] 
training-hugging-face-dlsa-weekly-1  | [0] 
training-hugging-face-dlsa-weekly-1  | [0] **********************************************************************
training-hugging-face-dlsa-weekly-1  | [0] '----Init tokenizer' took 4.970s (4,970,280,030ns)
training-hugging-face-dlsa-weekly-1  | [0] **********************************************************************
training-hugging-face-dlsa-weekly-1  | [0] 
training-hugging-face-dlsa-weekly-1  | [0] 
training-hugging-face-dlsa-weekly-1  | [0] **********************************************************************
training-hugging-face-dlsa-weekly-1  | [0] '----Tokenize + Extract Features' took 2.224s (2,224,425,317ns)
training-hugging-face-dlsa-weekly-1  | [0] **********************************************************************
training-hugging-face-dlsa-weekly-1  | [0] 
training-hugging-face-dlsa-weekly-1  | [0] 
training-hugging-face-dlsa-weekly-1  | [0] **********************************************************************
training-hugging-face-dlsa-weekly-1  | [0] 'Pre-process' took 7.195s (7,194,751,782ns)
training-hugging-face-dlsa-weekly-1  | [0] **********************************************************************
training-hugging-face-dlsa-weekly-1  | [0] 
training-hugging-face-dlsa-weekly-1  | [0] 
training-hugging-face-dlsa-weekly-1  | [0] **********************************************************************
training-hugging-face-dlsa-weekly-1  | [0] 'Load Model' took 18.566s (18,565,982,647ns)
training-hugging-face-dlsa-weekly-1  | [0] **********************************************************************
training-hugging-face-dlsa-weekly-1  | [0] 
training-hugging-face-dlsa-weekly-1  | [0] 
training-hugging-face-dlsa-weekly-1  | [0] **********************************************************************
training-hugging-face-dlsa-weekly-1  | [0] 'Fine-Tune' took 3708.674s (3,708,674,041,531ns)
training-hugging-face-dlsa-weekly-1  | [0] **********************************************************************
training-hugging-face-dlsa-weekly-1  | [0] 
training-hugging-face-dlsa-weekly-1  | [0] 
training-hugging-face-dlsa-weekly-1  | [0] **********************************************************************
training-hugging-face-dlsa-weekly-1  | [0] 'Inference' took 22.203s (22,203,208,806ns)
training-hugging-face-dlsa-weekly-1  | [0] **********************************************************************
training-hugging-face-dlsa-weekly-1  | [0] 
training-hugging-face-dlsa-weekly-1  | [0] 
training-hugging-face-dlsa-weekly-1  | [0] **********************************************************************
training-hugging-face-dlsa-weekly-1  | [0] 'Total Run' took 3759.048s (3,759,047,682,138ns)
training-hugging-face-dlsa-weekly-1  | [0] **********************************************************************
training-hugging-face-dlsa-weekly-1  | [0] 
training-hugging-face-dlsa-weekly-1  | [0] 
training-hugging-face-dlsa-weekly-1  | [0] 
training-hugging-face-dlsa-weekly-1  | [0] 
training-hugging-face-dlsa-weekly-1  | [0] ******** TEST METRICS ********
training-hugging-face-dlsa-weekly-1  | [0] test_loss: 0.2152438908815384
training-hugging-face-dlsa-weekly-1  | [0] test_acc: 0.9323394495412844
training-hugging-face-dlsa-weekly-1  | [0] test_runtime: 22.2013
training-hugging-face-dlsa-weekly-1  | [0] test_samples_per_second: 39.277
training-hugging-face-dlsa-weekly-1  | [0] test_steps_per_second: 4.91
training-hugging-face-dlsa-weekly-1  | [0] test_samples: 872
training-hugging-face-dlsa-weekly-1  | End Time:    Wed Jul 27 21:13:10 UTC 2022
training-hugging-face-dlsa-weekly-1  | Total Time: 62 min and 41 sec
training-hugging-face-dlsa-weekly-1 exited with code 0
```
