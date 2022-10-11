# Video-Streamer
## **Description**
This Pipeline provides the containerized implementation of a video streamer service. 

The workload aims to implement end-to-end video streamer pipeline involving media and analytics segments using GStreamer and TensorFlow. The pipeline handles video decode and processing followed by object detection and classification using the ssd-mobilenet-resnet-34 model using TensorFlow for single and multiple instances in FP32, BF16 and INT8 precisions. The metadata generated is uploaded to VDMS. For more information, go to [Video-Streamer](https://github.com/intel-innersource/frameworks.ai.end2end-ai-pipelines.video-streamer) GitHub repository. 

This pipeline uses two docker containers. The first container `vuiseng9/intellabs-vdms:demo-191220` enables an inference endpoint via port 55555 that receives the metadata generated as a result of inference launched by the second container `amr-registry.caas.intel.com/aiops/video-streamer:inference-centos-8`

## **Pull Docker Images**
```
docker pull vuiseng9/intellabs-vdms:demo-191220
docker pull amr-registry.caas.intel.com/aiops/video-streamer:inference-centos-8
```

## **Quick Start Scripts**

Script Name    | Description             | 
:----------------:|:------------------: | 
`benchmark.sh`    | The script collects performance characterization data on a target hardware platform | 

## **Download Dataset**
```
mkdir video_file
wget https://github.com/intel-iot-devkit/sample-videos/raw/master/classroom.mp4 -P video_file
export VIDEO=$(basename ${PWD}/video_file/classroom.mp4)
```

## **Download Models**
```
git clone https://github.com/intel-innersource/frameworks.ai.end2end-ai-pipelines.video-streamer.git .
git checkout v0.2.0
mkdir models
wget https://storage.googleapis.com/intel-optimized-tensorflow/models/v1_8/ssd_resnet34_fp32_1200x1200_pretrained_model.pb -P models
wget https://storage.googleapis.com/intel-optimized-tensorflow/models/v1_8/ssd_resnet34_int8_1200x1200_pretrained_model.pb -P models
```
## **Running with Docker**

The snippets below shows the quick start script running inside the container.

* Initiate the VDMS inference endpoint.

```
numactl --physcpubind=52-55 --membind=1 docker run --net=host -d vuiseng9/intellabs-vdms:demo-191220
```

* Initiate the Video-Streamer service.

```
#Create output directory to store results of inference
export OUTPUT_DIR=/output

#Run the quick start script using the docker image
docker run  \
  --env http_proxy=${http_proxy}  \
  --env https_proxy=${https_proxy}  \
  --env no_proxy=${no_proxy}  \
  --env VIDEO_FILE=/workspace/video-streamer/${VIDEO}  \
  --rm -it --privileged --net=host -p 55555:55555  \
  --volume ${PWD}/video-streamer:/workspace/video-streamer  \
  --volume ${PWD}/video_file/classroom.mp4:/workspace/video-streamer/${VIDEO}  \
  --volume ${OUTPUT_DIR}:${OUTPUT_DIR}  \
  -w /workspace/video-streamer  \
  amr-registry.caas.intel.com/aiops/video-streamer:inference-centos-8  \
  /bin/bash ./benchmark.sh && cp -r ../*.txt ${OUTPUT_DIR}
```

+++IMPORTANT:THE SECTION BELOW NEEDS TO BE UPDATED ONCE PUBLIC-FACING LINKS ARE MADE AVAILABLE +++
## **Documentation and Sources**

### **Get Started**
[Docker* Repository](https://hub.docker.com/u/intel) <br>
[Main GitHub*](https://github.com/intel-innersource/frameworks.ai.end2end-ai-pipelines.video-streamer)<br>
[Readme](https://github.com/intel-innersource/frameworks.ai.end2end-ai-pipelines.video-streamer/blob/master/README.md)<br>
[`<Release Notes>`](`<Link to Release Notes>`)<br>

### **Code Sources**
[Dockerfile](https://github.com/intel-innersource/frameworks.ai.infrastructure.machine-learning-operations/blob/develop/pipelines/video_analytics/tensorflow/ssd_resnet34/inference/Dockerfile.video-streamer)<br>
[Report Issue](https://community.intel.com/t5/Intel-Optimized-AI-Frameworks/bd-p/optimized-ai-frameworks)<br>

## **License Agreement**
LEGAL NOTICE: By accessing, downloading or using this software and any required dependent software (the “Software Package”), you agree to the terms and conditions of the software license agreements for the Software Package, which may also include notices, disclaimers, or license terms for third party software included with the Software Package. Please refer to the [license file](https://github.com/intel-innersource/frameworks.ai.infrastructure.machine-learning-operations/blob/develop/LICENSE) for additional details.

## **Related Containers and Solutions**
[View All Containers and Solutions 🡢](https://www.intel.com/content/www/us/en/developer/tools/software-catalog/containers.html)
