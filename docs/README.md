# Intel AI Containers
This page provides overview of AI Containers for many Intel 
optiomized open-source frameworks such as PyTorch, TensorFlow, SciKit Learn, 
XGBoost, Modin etc. Also provides containers for open-source deep learning models 
optimized by Intel to run on Intel® Xeon® Scalable processors and Intel® Data Center GPUs.
## Intel® Distribution of Python
Docker container with Intel® Distribution of Python
|              Container             |Framework|           Docker Pull Command           |Compressed Size|
|------------------------------------|---------|-----------------------------------------|---------------|
|Intel® Distribution of Python - Full|    -    |```docker pull intel/python:py310-full```|     1.38GB    |
|Intel® Distribution of Python - Core|    -    |```docker pull intel/python:py310-core```|    814.77MB   |
## Intel® CPU Base Containers
Base containers to run on Intel® Xeon® Scalable processors
|                                Container                               | Framework|                              Docker Pull Command                              |Compressed Size|
|------------------------------------------------------------------------|----------|-------------------------------------------------------------------------------|---------------|
|                Intel® Optimizations for TensorFlow (PIP)               |TensorFlow|       ```docker pull intel/intel-optimized-tensorflow:2.14.0-pip-base```      |    405.53MB   |
|Intel® Optimizations for TensorFlow with Jupyter  notebook support (PIP)|TensorFlow|     ```docker pull intel/intel-optimized-tensorflow:2.14.0-pip-jupyter```     |     464MB     |
|    Intel® Optimizations for TensorFlow Multi-node with OpenMPI (PIP)   |TensorFlow|```docker pull intel/intel-optimized-tensorflow:2.14.0-pip-openmpi-multinode```|     817MB     |


[Complete list of Containers](CPU_Base_Containers.md)

## Intel® GPU Base Containers
Intel® Data Center GPU Max Series and Intel® Data Center GPU Flex Series base containers
|                                                                      Container                                                                     |Framework|                    Docker Pull Command                   |Compressed Size|
|----------------------------------------------------------------------------------------------------------------------------------------------------|---------|----------------------------------------------------------|---------------|
|[Intel® Extension for PyTorch* Container for Flex Series](https://github.com/intel/intel-extension-for-pytorch/blob/v2.0.110%2Bxpu/docker/README.md)| PyTorch |  ```docker pull intel-extension-for-pytorch:xpu-flex```  |     7.04GB    |
| [Intel® Extension for PyTorch* Container for Max Series](https://github.com/intel/intel-extension-for-pytorch/blob/v2.0.110%2Bxpu/docker/README.md)| PyTorch |   ```docker pull intel-extension-for-pytorch:xpu-max```  |     7.13GB    |
|             [Intel® Extension for TensorFlow](https://github.com/intel/intel-extension-for-tensorflow/blob/v2.13.0.0/docker/README.md)             |TensoFlow|```docker pull intel/intel-extension-for-tensorflow:xpu```|     2.29GB    |


[Complete list of Containers](GPU_Base_Containers.md)

## Intel® CPU Model Containers
These are the deep learning Models optimized to run on Intel® Xeon® Scalable processors
|                                                                         Container                                                                         | Framework|                              Docker Pull Command                             |Compressed Size|
|-----------------------------------------------------------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------|---------------|
| [ResNet 50v1.5 Training](https://github.com/IntelAI/models/blob/r3.1/quickstart/image_recognition/tensorflow/resnet50v1_5/training/cpu/README_DEV_CAT.md) |TensorFlow| ```docker pull intel/image-recognition:centos-tf-cpu-resnet50v1-5-training```|     1.46GB    |
|[ResNet 50v1.5 Inference](https://github.com/IntelAI/models/blob/r3.1/quickstart/image_recognition/tensorflow/resnet50v1_5/inference/cpu/README_DEV_CAT.md)|TensorFlow|```docker pull intel/image-recognition:centos-tf-cpu-resnet50v1-5-inference```|     1.69GB    |
|    [BERT large Training](https://github.com/IntelAI/models/blob/r3.1/quickstart/language_modeling/tensorflow/bert_large/training/cpu/README_DEV_CAT.md)   |TensorFlow|```docker pull intel/language-modeling:centos-tf-cpu-bert-large-pretraining```|     1.46GB    |


[Complete list of Containers](CPU_Models_Containers.md)

## Intel® Flex (ATSM) Model Containers
These are the deep learning Models optimized to run on Intel's Flex Series GPU platform.
|                                                                           Container                                                                           | Framework|                             Docker Pull Command                            |Compressed Size|
|---------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|----------------------------------------------------------------------------|---------------|
|[ResNet50 v1.5 Inference](https://github.com/IntelAI/models/blob/v2.12.1/quickstart/image_recognition/tensorflow/resnet50v1_5/inference/gpu/DEVCATALOG_FLEX.md)|TensorFlow|```docker pull intel/image-recognition:tf-flex-gpu-resnet50v1-5-inference```|    2.36 GB    |
|       [MaskRCNN Inference](https://github.com/IntelAI/models/blob/v2.12.1/quickstart/image_segmentation/tensorflow/maskrcnn/inference/gpu/DEVCATALOG.md)      |TensorFlow|  ```docker pull intel/image-segmentation:tf-flex-gpu-maskrcnn-inference``` |     2.72GB    |
|   [EfficientNet Inference](https://github.com/IntelAI/models/blob/v2.12.1/quickstart/image_recognition/tensorflow/efficientnet/inference/gpu/DEVCATALOG.md)   |TensorFlow|```docker pull intel/image-recognition:tf-flex-gpu-efficientnet-inference```|    2.32 GB    |


[Complete list of Containers](Flex_Models_Containers.md)

## Intel® Max (PVC) Model Containers
These are the deep learning Models optimized to run on Intel's Max Series GPU platform.
|                                                                         Container                                                                        |Framework|                               Docker Pull Command                              |Compressed Size|
|----------------------------------------------------------------------------------------------------------------------------------------------------------|---------|--------------------------------------------------------------------------------|---------------|
|[ResNet50 v1.5 Inference](https://github.com/IntelAI/models/blob/master/quickstart/image_recognition/pytorch/resnet50v1_5/inference/gpu/DEVCATALOG_MAX.md)| PyTorch |```docker pull intel/image-recognition:pytorch-max-gpu-resnet50v1-5-inference```|     2.17GB    |
|   [ResNet50 v1.5 Training](https://github.com/IntelAI/models/blob/master/quickstart/image_recognition/pytorch/resnet50v1_5/training/gpu/DEVCATALOG.md)   | PyTorch | ```docker pull intel/image-recognition:pytorch-max-gpu-resnet50v1-5-training```|     2.31GB    |
|     [BERT Large Inference](https://github.com/IntelAI/models/blob/master/quickstart/language_modeling/pytorch/bert_large/inference/gpu/DEVCATALOG.md)    | PyTorch | ```docker pull intel/language-modeling:pytorch-max-gpu-bert-large-inference``` |     2.21GB    |


[Complete list of Containers](Max_Models_Containers.md)

## Intel® AI Tools
These are Domain Toolkit Containers that use the latest transformers and LLM technology with Intel optimizations.
|                                                                Container                                                                |      Framework     |              Docker Pull Command             |Compressed Size|
|-----------------------------------------------------------------------------------------------------------------------------------------|--------------------|----------------------------------------------|---------------|
|              [Intel® Transfer Learning Toolkit](https://github.com/IntelAI/transfer-learning/blob/v0.5.0/docker/README.md)              |PyTorch & TensorFlow|  ```docker pull intel/ai-tools:tlt-0.5.0```  |    910.64MB   |
|[Intel® Extension for Transformers Chatbot](https://github.com/intel/intel-extension-for-transformers/blob/main/docker/README_chatbot.md)|PyTorch & TensorFlow|```docker pull intel/ai-tools:itrex-chatbot```|     4.54GB    |
|        [Intel® Extension for Transformers](https://github.com/intel/intel-extension-for-transformers/blob/main/docker/README.md)        |PyTorch & TensorFlow| ```docker pull intel/ai-tools:itrex-1.3.0``` |     1.04GB    |


[Complete list of Containers](AI_Tools_Containers.md)

## Intel® AI Tools Selector Preset Containers
Intel® AI Tools Selector Preset Containers provides development environment with Intel optimized software for data scientists and developers.
|                                         Container                                        |Framework|                 Docker Pull Command                |Compressed Size|
|------------------------------------------------------------------------------------------|---------|----------------------------------------------------|---------------|
| [Data Analytics py3.9](https://github.com/intel/ai-containers/blob/main/preset/README.md)|    -    | ```docker pull intel/data-analytics:latest-py3.9```|     1.97GB    |
|[Data Analytics py3.10](https://github.com/intel/ai-containers/blob/main/preset/README.md)|    -    |```docker pull intel/data-analytics:latest-py3.10```|     1.98GB    |
|  [Classical ML py3.9](https://github.com/intel/ai-containers/blob/main/preset/README.md) |    -    |  ```docker pull intel/classical-ml:latest-py3.9``` |     2.11GB    |


[Complete list of Containers](Preset_Containers.md)

## Intel® AI Workflows
These containers are for domain use-cases like Disease Prediction, Credit Card Fraud Detection, and Document Automation.
|                                             Container                                             |Framework|                      Docker Pull Command                      |Compressed Size|
|---------------------------------------------------------------------------------------------------|---------|---------------------------------------------------------------|---------------|
|[Document Automation Fine Tuning](https://github.com/intel/document-automation/blob/main/README.md)|    -    |```docker pull intel/ai-workflows:doc-automation-fine-tuning```|     2.53GB    |
|  [Document Automation Indexing](https://github.com/intel/document-automation/blob/main/README.md) |    -    |  ```docker pull intel/ai-workflows:doc-automation-indexing``` |     3.03GB    |
|  [Fraud Detection GNN](https://github.com/intel/credit-card-fraud-detection/blob/main/README.md)  |    -    |  ```docker pull intel/ai-workflows:pa-fraud-detection-gnn```  |     2.1GB     |


[Complete list of Containers](AI_Workflow_Containers.md)

