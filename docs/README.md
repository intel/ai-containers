# Intel AI Containers
This page provides overview of AI Containers for many Intel 
optiomized open-source frameworks such as PyTorch, TensorFlow, SciKit Learn, 
XGBoost, Modin etc. Also provides containers for open-source deep learning models 
optimized by Intel to run on Intel® Xeon® Scalable processors and Intel® Data Center GPUs.
## Intel® Web Configurator Preset Containers
Intel® Web Configurator Preset Containers provides development environment with Intel optimized software for data scientists and developers.
|                                     Container                                     |Framework|                 Docker Pull Command                |Compressed Size|
|-----------------------------------------------------------------------------------|---------|----------------------------------------------------|---------------|
|[Data Analytics](https://github.com/intel/ai-containers/blob/main/preset/README.md)|   None  | ```docker pull intel/data-analytics:2023.2-py3.9```|     1.24GB    |
|[Data Analytics](https://github.com/intel/ai-containers/blob/main/preset/README.md)|   None  |```docker pull intel/data-analytics:2023.2-py3.10```|     1.25GB    |
| [Classical ML](https://github.com/intel/ai-containers/blob/main/preset/README.md) |   None  |  ```docker pull intel/classical-ml:2023.2-py3.9``` |     1.42GB    |


[Complete list of GPU base containers](Preset_Containers.md)

## Intel® Distribution of Python
Docker container with Intel® Distribution of Python
|              Container             |Framework|           Docker Pull Command           |Compressed Size|
|------------------------------------|---------|-----------------------------------------|---------------|
|Intel® Distribution of Python - Full|    -    |```docker pull intel/python:py310-full```|     1.38GB    |
|Intel® Distribution of Python - Core|    -    |```docker pull intel/python:py310-core```|     867MB     |
## Intel GPU Base Containers
Intel® Data Center GPU Max Series and Intel® Data Center GPU Flex Series base containers
|                                                                      Container                                                                     |Framework|                    Docker Pull Command                   |Compressed Size|
|----------------------------------------------------------------------------------------------------------------------------------------------------|---------|----------------------------------------------------------|---------------|
|[Intel® Extension for PyTorch* Container for Flex Series](https://github.com/intel/intel-extension-for-pytorch/blob/v2.0.110%2Bxpu/docker/README.md)| PyTorch |  ```docker pull intel-extension-for-pytorch:xpu-flex```  |     7.04GB    |
| [Intel® Extension for PyTorch* Container for Max Series](https://github.com/intel/intel-extension-for-pytorch/blob/v2.0.110%2Bxpu/docker/README.md)| PyTorch |   ```docker pull intel-extension-for-pytorch:xpu-max```  |     7.13GB    |
|             [Intel® Extension for TensorFlow](https://github.com/intel/intel-extension-for-tensorflow/blob/v2.13.0.0/docker/README.md)             |TensoFlow|```docker pull intel/intel-extension-for-tensorflow:xpu```|     2.29GB    |


[Complete list of GPU base containers](GPU_Base_Containers.md)

## Intel CPU Base Containers
Base containers to run on Intel® Xeon® Scalable processors
|                                Container                               | Framework|                             Docker Pull Command                             |Compressed Size|
|------------------------------------------------------------------------|----------|-----------------------------------------------------------------------------|---------------|
|                Intel® Optimizations for TensorFlow (PIP)               |TensorFlow|       ```docker pull intel/intel-optimized-tensorflow:2.13-pip-base```      |     412MB     |
|Intel® Optimizations for TensorFlow with Jupyter  notebook support (PIP)|TensorFlow|     ```docker pull intel/intel-optimized-tensorflow:2.13-pip-jupyter```     |     465MB     |
|   Intel® Optimizations for TensorFlow Multi-node with OpenMPI  (PIP)   |TensorFlow|```docker pull intel/intel-optimized-tensorflow:2.13-pip-openmpi-multinode```|     820MB     |


[Complete list of GPU base containers](CPU_Base_Containers.md)

## Intel Flex (ATSM) Models Containers
These are the deep learning Models optimized to run on Intel's Flex Series GPU platform.
|                                                                           Container                                                                           | Framework|                             Docker Pull Command                            |Compressed Size|
|---------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|----------------------------------------------------------------------------|---------------|
|[ResNet50 v1.5 Inference](https://github.com/IntelAI/models/blob/v2.12.1/quickstart/image_recognition/tensorflow/resnet50v1_5/inference/gpu/DEVCATALOG_FLEX.md)|TensorFlow|```docker pull intel/image-recognition:tf-flex-gpu-resnet50v1-5-inference```|    2.36 GB    |
|       [MaskRCNN Inference](https://github.com/IntelAI/models/blob/v2.12.1/quickstart/image_segmentation/tensorflow/maskrcnn/inference/gpu/DEVCATALOG.md)      |TensorFlow|  ```docker pull intel/image-segmentation:tf-flex-gpu-maskrcnn-inference``` |     2.72GB    |
|   [EfficientNet Inference](https://github.com/IntelAI/models/blob/v2.12.1/quickstart/image_recognition/tensorflow/efficientnet/inference/gpu/DEVCATALOG.md)   |TensorFlow|```docker pull intel/image-recognition:tf-flex-gpu-efficientnet-inference```|    2.32 GB    |


[Complete list of GPU base containers](Flex_Models_Containers.md)

## Intel Max (PVC) Models Containers
These are the deep learning Models optimized to run on Intel's Max Series GPU platform.
|                                                                         Container                                                                        |Framework|                               Docker Pull Command                              |Compressed Size|
|----------------------------------------------------------------------------------------------------------------------------------------------------------|---------|--------------------------------------------------------------------------------|---------------|
|[ResNet50 v1.5 Inference](https://github.com/IntelAI/models/blob/master/quickstart/image_recognition/pytorch/resnet50v1_5/inference/gpu/DEVCATALOG_MAX.md)| PyTorch |```docker pull intel/image-recognition:pytorch-max-gpu-resnet50v1-5-inference```|     2.17GB    |
|   [ResNet50 v1.5 Training](https://github.com/IntelAI/models/blob/master/quickstart/image_recognition/pytorch/resnet50v1_5/training/gpu/DEVCATALOG.md)   | PyTorch | ```docker pull intel/image-recognition:pytorch-max-gpu-resnet50v1-5-training```|     2.31GB    |
|     [BERT Large Inference](https://github.com/IntelAI/models/blob/master/quickstart/language_modeling/pytorch/bert_large/inference/gpu/DEVCATALOG.md)    | PyTorch | ```docker pull intel/language-modeling:pytorch-max-gpu-bert-large-inference``` |     2.21GB    |


[Complete list of GPU base containers](Max_Models_Containers.md)

## Intel CPU Models Containers
These are the deep learning Models optimized to run on Intel® Xeon® Scalable processors
|                                                                            Container                                                                            | Framework|                          Docker Pull Command                          |Compressed Size|
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|-----------------------------------------------------------------------|---------------|
| [ResNet 50v1.5 Training](https://github.com/IntelAI/models/blob/master/quickstart/image_recognition/tensorflow/resnet50v1_5/training/cpu/README_SPR_DEV_CAT.md) |TensorFlow| ```docker pull intel/image-recognition:tf-spr-resnet50v1-5-training```|     630MB     |
|[ResNet 50v1.5 Inference](https://github.com/IntelAI/models/blob/master/quickstart/image_recognition/tensorflow/resnet50v1_5/inference/cpu/README_SPR_DEV_CAT.md)|TensorFlow|```docker pull intel/image-recognition:tf-spr-resnet50v1-5-inference```|     717MB     |
|    [BERT large Training](https://github.com/IntelAI/models/blob/master/quickstart/language_modeling/tensorflow/bert_large/training/cpu/README_SPR_DEV_CAT.md)   |TensorFlow|```docker pull intel/language-modeling:tf-spr-bert-large-pretraining```|     593MB     |


[Complete list of GPU base containers](CPU_Models_Containers.md)

