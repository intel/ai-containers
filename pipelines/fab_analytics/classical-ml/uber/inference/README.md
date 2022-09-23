# Classical ML PyUber INFERENCE - Wafer Insights
## Description
This document contains instructions on how to run Wafer Insights pipelines with make and docker compose.
## Project Structure 
```
├── wafer-insights @ WorkflowI6
├── docker-compose.yml
├── Dockerfile.wafer-insights
├── Makefile
└── README.md
```
[_Makefile_](Makefile)
```
OUTPUT_DIR ?= /output
FINAL_IMAGE_NAME ?= wafer-insights

wafer-insight:
	@OUTPUT_DIR=${OUTPUT_DIR} \
	 FINAL_IMAGE_NAME=${FINAL_IMAGE_NAME} \
 	 docker compose up wafer-insight --build

clean: 
	docker compose down
```
[_docker-compose.yml_](docker-compose.yml)
```
services:
  wafer-insight:
    build:
      args: 
        http_proxy: ${http_proxy}
        https_proxy: ${https_proxy}
        no_proxy: ${no_proxy}
      dockerfile: Dockerfile.wafer-insights
    command: 
    - |
      conda run -n WI python src/loaders/synthetic_loader/loader.py
      conda run --no-capture-output -n WI python src/dashboard/app.py
    entrypoint: ["/bin/bash", "-c"]
    environment: 
      - PYTHONPATH=$PYTHONPATH:$PWD
      - http_proxy=${http_proxy}
      - https_proxy=${https_proxy}
      - no_proxy=${no_proxy}
    image: ${FINAL_IMAGE_NAME}:inference-ubuntu-20.04
    ports: 
      - 8050:8050
    privileged: true
    volumes: 
      - ${OUTPUT_DIR}:/data
      - ./wafer-insights:/workspace/wafer-insights
    working_dir: /workspace/wafer-insights
```

# Wafer Insights
End2End AI Workflow utilizing a Flask dashboard to allow users to predict FMAX/IDV tokens based on FAB data sources. More information [here](https://github.com/intel-sandbox/applications.ai.appliedml.workflow.waferinsights/tree/WorkflowI6)

## Quick Start
* Pull and configure the dependent repo submodule `git submodule update --init --recursive`.

* Install [Pipeline Repository Dependencies](https://github.com/intel-innersource/frameworks.ai.infrastructure.machine-learning-operations/blob/develop/pipelines/README.md)

* Get the public IP address of your machine with either `ip a` or https://whatismyipaddress.com/

* Other variables:

| Variable Name | Default | Notes |
| --- | --- | --- |
| FINAL_IMAGE_NAME | `wafer-insights` | Final Docker image name |
| OUTPUT_DIR | `/output` | Output directory |

## Build and Run
Build and Run with defaults:
```
make wafer-insight
```

* Visit the dashboard at your public ip address and port `8050`.

## Build and Run Example
```
$ make wafer-insight
WARN[0000] The "PYTHONPATH" variable is not set. Defaulting to a blank string. 
[+] Building 0.1s (9/9) FINISHED                                                                                 
 => [internal] load build definition from Dockerfile.wafer-insights                                         0.0s
 => => transferring dockerfile: 47B                                                                         0.0s
 => [internal] load .dockerignore                                                                           0.0s
 => => transferring context: 2B                                                                             0.0s
 => [internal] load metadata for docker.io/library/ubuntu:20.04                                             0.0s
 => [1/5] FROM docker.io/library/ubuntu:20.04                                                               0.0s
 => CACHED [2/5] RUN apt-get update && apt-get install --no-install-recommends --fix-missing -y     ca-cer  0.0s
 => CACHED [3/5] RUN mkdir -p /workspace                                                                    0.0s
 => CACHED [4/5] RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O  0.0s
 => CACHED [5/5] RUN conda create -yn WI python=3.9 &&     source activate WI &&     conda install -y scik  0.0s
 => exporting to image                                                                                      0.0s
 => => exporting layers                                                                                     0.0s
 => => writing image sha256:dfa7411736694db4d3c8d0032f424fc88f0af98fabd163a659a90d0cc2dfe587                0.0s
 => => naming to docker.io/library/wafer-insights:inference-ubuntu-20.04                                    0.0s
WARN[0000] Found orphan containers ([inference-wafer-analytics-1]) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up. 
[+] Running 1/1
 ⠿ Container inference-wafer-insight-1  Recreated                                                           0.1s
Attaching to inference-wafer-insight-1
inference-wafer-insight-1  | [[-5.39543860e-04  2.39971569e-03 -3.42210731e-04 ... -2.35041980e-03
inference-wafer-insight-1  |   -1.81397056e-04 -2.09303234e-03]
inference-wafer-insight-1  |  [-1.00075542e-04 -5.41824409e-04 -2.38435358e-04 ...  3.39901582e-03
inference-wafer-insight-1  |    3.35075678e-04  2.04678475e-03]
inference-wafer-insight-1  |  [-5.14076633e-04 -2.28770984e-03  3.52836617e-04 ... -3.59841471e-03
inference-wafer-insight-1  |   -2.57484490e-03  5.23169035e-04]
inference-wafer-insight-1  |  ...
inference-wafer-insight-1  |  [-3.13805323e-03 -3.16870576e-03  1.28447995e-03 ... -8.94258047e-05
inference-wafer-insight-1  |    8.13668371e-04 -5.02239567e-04]
inference-wafer-insight-1  |  [-7.28863425e-04  2.32030465e-03  1.57134892e-03 ...  2.64884040e-04
inference-wafer-insight-1  |   -2.12739801e-03 -1.98500740e-04]
inference-wafer-insight-1  |  [-1.79534321e-03  6.97006847e-04  4.70415219e-04 ... -4.21349858e-04
inference-wafer-insight-1  |    2.88895727e-03  4.20368128e-04]]
inference-wafer-insight-1  |    fcol`feature_0  fcol`feature_1  ...  fcol`feature_1999              TEST_END_DATE
inference-wafer-insight-1  | 0       -0.000540        0.002400  ...          -0.002093 2022-06-24 17:57:44.060832
inference-wafer-insight-1  | 1       -0.000100       -0.000542  ...           0.002047 2022-06-24 18:02:55.100832
inference-wafer-insight-1  | 2       -0.000514       -0.002288  ...           0.000523 2022-06-24 18:08:06.140832
inference-wafer-insight-1  | 3       -0.000020       -0.003073  ...           0.001036 2022-06-24 18:13:17.180832
inference-wafer-insight-1  | 4       -0.001280        0.001955  ...          -0.000343 2022-06-24 18:18:28.220832
inference-wafer-insight-1  | 
inference-wafer-insight-1  | [5 rows x 2001 columns]
inference-wafer-insight-1  | started_stacking
inference-wafer-insight-1  |            LOT7  WAFER3 PROCESS  ...    MEDIAN DEVREVSTEP TESTNAME`STRUCTURE_NAME
inference-wafer-insight-1  | 0  DG0000000001       0    1234  ... -0.000540      DPMLD          fcol`feature_0
inference-wafer-insight-1  | 1  DG0000000001       1    1234  ... -0.000100      DPMLD          fcol`feature_0
inference-wafer-insight-1  | 2  DG0000000001       2    1234  ... -0.000514      DPMLD          fcol`feature_0
inference-wafer-insight-1  | 3  DG0000000001       3    1234  ... -0.000020      DPMLD          fcol`feature_0
inference-wafer-insight-1  | 4  DG0000000001       4    1234  ... -0.001280      DPMLD          fcol`feature_0
inference-wafer-insight-1  | 
inference-wafer-insight-1  | [5 rows x 10 columns]
inference-wafer-insight-1  | 
inference-wafer-insight-1  | Dash is running on http://0.0.0.0:8050/
inference-wafer-insight-1  | 
inference-wafer-insight-1  |  * Serving Flask app 'app'
inference-wafer-insight-1  |  * Debug mode: on
```

## See results in your Browser

![pic](https://github.com/intel-innersource/frameworks.ai.infrastructure.machine-learning-operations/assets/43555799/0b3a2b8c-5355-47c7-8f50-7a75c8a5f48a)
