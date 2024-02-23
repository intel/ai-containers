# Intel® Flex (ATSM) Model Containers

These are the deep learning Models optimized to run on Intel's Flex Series GPU platform.

|                                                                          Container                                                                          | Framework|                               Docker Pull Command                               |Compressed Size|
|-------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|---------------------------------------------------------------------------------|---------------|
|          [ResNet50 v1.5 Inference](https://github.com/IntelAI/models/blob/v3.1.0/models_v2/tensorflow/resnet50v1_5/inference/gpu/CONTAINER_FLEX.md)         |TensorFlow|   ```docker pull intel/image-recognition:tf-flex-gpu-resnet50v1-5-inference```  |     2.35GB    |
|                 [MaskRCNN Inference](https://github.com/IntelAI/models/blob/v3.1.0/models_v2/tensorflow/maskrcnn/inference/gpu/CONTAINER.md)                |TensorFlow|    ```docker pull intel/image-segmentation:tf-flex-gpu-maskrcnn-inference```    |     2.59GB    |
|             [EfficientNet Inference](https://github.com/IntelAI/models/blob/v3.1.0/models_v2/tensorflow/efficientnet/inference/gpu/CONTAINER.md)            |TensorFlow|   ```docker pull intel/image-recognition:tf-flex-gpu-efficientnet-inference```  |     2.3GB     |
|         [Stable Diffusion Inference](https://github.com/IntelAI/models/blob/v3.1.0/models_v2/tensorflow/stable_diffusion/inference/gpu/CONTAINER.md)        |TensorFlow|   ```docker pull intel/generative-ai:tf-flex-gpu-stable-diffusion-inference```  |     2.54GB    |
|         [Wide and Deep Inference](https://github.com/IntelAI/models/blob/v3.1.0/models_v2/tensorflow/wide_deep_large_ds/inference/gpu/CONTAINER.md)         |TensorFlow|    ```docker pull intel/recommendation:tf-flex-gpu-wide-and-deep-inference```   |     2.33GB    |
| [ResNet50 v1.5 Inference](https://github.com/IntelAI/models/blob/v2.12.1/quickstart/image_recognition/pytorch/resnet50v1_5/inference/gpu/DEVCATALOG_FLEX.md)|  PyTorch |```docker pull intel/image-recognition:pytorch-flex-gpu-resnet50v1-5-inference```|     2.17GB    |
|          [YOLOv5 inference](https://github.com/IntelAI/models/blob/v2.12.1/quickstart/object_detection/pytorch/yolov5/inference/gpu/DEVCATALOG.md)          |  PyTorch |    ```docker pull intel/object-detection:pytorch-flex-gpu-yolov5-inference```   |     2.54GB    |
|        [Stable Diffusion inference](https://github.com/IntelAI/models/blob/v3.1.0/models_v2/pytorch/stable_diffusion/inference/gpu/CONTAINER_FLEX.md)       |  PyTorch |```docker pull intel/generative-ai:pytorch-flex-gpu-stable-diffusion-inference```|     2.65GB    |
|              [DistilBERT inference](https://github.com/IntelAI/models/blob/v3.1.0/models_v2/pytorch/distilbert/inference/gpu/CONTAINER_FLEX.md)             |  PyTorch | ```docker pull intel/language-modeling:pytorch-flex-gpu-distilbert-inference``` |     2.54GB    |
|                     [DLRM-v1 inference](https://github.com/IntelAI/models/blob/v3.1.0/models_v2/pytorch/dlrm/inference/gpu/CONTAINER.md)                    |  PyTorch |    ```docker pull intel/recommendation:pytorch-flex-gpu-dlrm-v1-inference```    |     2.58GB    |
|  [SSD-MobileNet v1 Inference](https://github.com/IntelAI/models/blob/v2.11.1/quickstart/object_detection/pytorch/ssd-mobilenet/inference/gpu/DEVCATALOG.md) |  PyTorch |```docker pull intel/object-detection:pytorch-flex-gpu-ssd-mobilenet-inference```|     2.47GB    |
|          [YOLOv4 inference](https://github.com/IntelAI/models/blob/v2.11.1/quickstart/object_detection/pytorch/yolov4/inference/gpu/DEVCATALOG.md)          |  PyTorch |    ```docker pull intel/object-detection:pytorch-flex-gpu-yolov4-inference```   |     2.56GB    |
|[SSD-MobileNet v1 Inference](https://github.com/IntelAI/models/blob/v2.11.1/quickstart/object_detection/tensorflow/ssd-mobilenet/inference/gpu/DEVCATALOG.md)|TensorFlow|   ```docker pull intel/object-detection:tf-flex-gpu-ssd-mobilenet-inference```  |     2.47GB    |

[Intel AI Containers](README.md)
