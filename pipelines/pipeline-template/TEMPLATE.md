# <FRAMEWORK> <DATASET> <MODE> - <Pipeline1, Pipeline2, ... and Pipeline3>
## Description
This document contains instructions on how to run <Pipeline1, Pipeline2, ... and Pipeline3> pipelines with make and docker compose.
## Project Structure 
```
├── <E2E_REPO> @ <BRANCH>
├── docker-compose.yml
├── Dockerfile.<PIPELINE_NAME>
├── Makefile
└── README.md
```
[_Makefile_](Makefile)
```
<ARG1> ?= <default_1>
<ARG2> ?= <default_2>
<ARG3> ?= <default_3>
FINAL_IMAGE_NAME ?= <PIPELINE_NAME>
OUTPUT_DIR ?= /output

<PIPELINE_NAME>:
	@<ARG1>=${<ARG1>} \
	 <ARG2>=${<ARG2>} \
	 <ARG3>=${<ARG3>} \
	 FINAL_IMAGE_NAME=${FINAL_IMAGE_NAME} \
	 OUTPUT_DIR=${OUTPUT_DIR} \
 	 docker compose up <PIPELINE_NAME> --build

clean: 
	docker compose down
```
[_docker-compose.yml_](docker-compose.yml)
```
services:
  <PIPELINE_NAME>:
    build:
      args: 
        <ARG1>: ${<ARG1>}
        <ARG2>: ${<ARG2>}
        http_proxy: ${http_proxy}
        https_proxy: ${https_proxy}
        no_proxy: ${no_proxy}
      dockerfile: Dockerfile.<PIPELINE_NAME>
    command: /workspace/<E2E_REPO>/<PIPELINE_SCRIPT>.sh ${<ARG1>}
    environment: 
      - ${<ARG1>}=${<ARG1>}
      - ${<ARG3>}=${<ARG3>}
      - http_proxy=${http_proxy}
      - https_proxy=${https_proxy}
      - no_proxy=${no_proxy}
    image: ${FINAL_IMAGE_NAME}:<MODE>-<BASE_IMAGE_NAME>-<BASE_IMAGE_TAG>
    privileged: true
    volumes: 
      - ${OUTPUT_DIR}:${OUTPUT_DIR}
      - ./<E2E_REPO>:/workspace/<E2E_REPO>
    working_dir: /workspace/<E2E_REPO>
```

# <PIPELINE_NAME>
End2End AI Workflow utilizing <TECHNOLOGY>. More information [here](<E2E_REPO>)

## Quick Start
* Pull and configure the dependent repo submodule `git submodule update --init --recursive`.

* Install [Pipeline Repository Dependencies](https://github.com/intel-innersource/frameworks.ai.infrastructure.machine-learning-operations/blob/develop/pipelines/README.md)

* Other variables:

| Variable Name | Default | Notes |
| --- | --- | --- |
| FINAL_IMAGE_NAME | `<PIPELINE_NAME>` | Final Docker image name |
| OUTPUT_DIR | `/output` | Output directory |
| <ARG1> | `<default_value1>` | |
| <ARG2> | `<default_value2>` | |
| <ARG3> | `<default_value3>` | |
## Build and Run
Build and Run with defaults:
```
make <PIPELINE_NAME>
```
## Build and Run Example
```
<Start of Expected Ouput>
```
...
```
<End of Expected Output>
```
