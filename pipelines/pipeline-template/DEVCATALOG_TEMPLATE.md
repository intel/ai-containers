# **Title**

## **Description**
Short description and provide link to [Main Repository](<Link to Main GitHub Repository>)

## **Pull Docker Image**
```
docker pull <Docker image name>
```

## **Download Model**
Clone [Main Repository](<Link to Main GitHub Repository>) repository into your working directory.
```
git clone <e2e_repo.git> .
```
## Download Dataset
`<Direction on Downloading Dataset>`

## **Quick Start Scripts**
| Script Name | Description | 
| --- | --- |
| `script1.sh` | Description | 
| `script2.sh` | Description | 

## **Customization Options**
Include any other options need to run the workflow, such as downloading dataset, models, etc.

## **Running with Docker**
`<Direction on Running Docker Container(s)>`
```
export DATASET_DIR=<path to the dataset>
export OUTPUT_DIR=<directory where the output log files will be written>

docker run \
  --env DATASET_DIR=${DATASET_DIR} \
  --env OUTPUT_DIR=${OUTPUT_DIR} \
  --env http_proxy=${http_proxy} \
  --env https_proxy=${https_proxy} \
  --env no_proxy=${no_proxy} \
  --volume ${DATASET_DIR}:/data \
  --volume ${OUTPUT_DIR}:/output \
  --volume $(pwd):/workspace \
  --workdir /workspace \
  --privileged --init -it \
  <Docker image name> \
  ./${SCRIPT}
```
## **Documentation and Sources**

### **Get Started**
[`<Docker* Repository>`](`<Link to Docker image on DockerHub or other hubs>`) <br>
[`<Main GitHub*>`](`<Link to Main GitHub Repository>`)<br>
[`<Readme>`](`<Link to Main GitHub Repository README.md>`)<br>
[`<Release Notes>`](`<Link to Release Notes>`)<br>

### **Code Sources**
[`<Dockerfile>`](`<Link to Docker file>`)<br>
[Report Issue](https://community.intel.com/t5/Intel-Optimized-AI-Frameworks/bd-p/optimized-ai-frameworks)<br>

## **License Agreement**
LEGAL NOTICE: By accessing, downloading or using this software and any required dependent software (the “Software Package”), you agree to the terms and conditions of the software license agreements for the Software Package, which may also include notices, disclaimers, or license terms for third party software included with the Software Package. Please refer to the [license file](https://github.com/intel-innersource/frameworks.ai.infrastructure.machine-learning-operations/blob/develop/LICENSE) for additional details.

## **Related Containers and Solutions**
[View All Containers and Solutions 🡢](https://www.intel.com/content/www/us/en/developer/tools/software-catalog/containers.html)