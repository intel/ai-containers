# Intel® Extension for TensorFlow\*

These are containers with **Intel® Extension for TensorFlow\*** pre-installed.

**Intel® Extension for TensorFlow\*** is a heterogeneous, high performance deep learning extension plugin based on TensorFlow [PluggableDevice](https://github.com/tensorflow/community/blob/master/rfcs/20200624-pluggable-device-for-tensorflow.md) interface to bring Intel XPU(GPU, CPU, etc.) devices into [TensorFlow](https://github.com/tensorflow/tensorflow) open source community for AI workload acceleration. It allows flexibly plugging an XPU into TensorFlow on-demand, and exposing computing power inside Intel's hardware.

## Pull and start the XPU Docker container

```bash
docker pull intel/intel-extension-for-tensorflow:xpu
docker run -it -p 8888:8888 --device /dev/dri -v /dev/dri/by-path:/dev/dri/by-path --ipc=host intel/intel-extension-for-tensorflow:xpu
```

## Pull and start the CPU Docker container

```bash
docker pull intel/intel-extension-for-tensorflow:cpu
docker run -it -p 8888:8888 intel/intel-extension-for-tensorflow:cpu
```

## Pull and start the Intel® Extension for TensorFlow\* Serving GPU Docker container

```bash
docker pull intel/intel-extension-for-tensorflow:serving-gpu
docker run -it -p 8500:8500 --device /dev/dri -v /dev/dri/by-path:/dev/dri/by-path -e MODEL_NAME=<your-model-name> -e MODEL_DIR=<your-model-dir> intel/intel-extension-for-tensorflow:serving-gpu
```

For more details, follow the procedure in [Intel® Extension for TensorFlow\* Serving](https://intel.github.io/intel-extension-for-tensorflow/latest/docker/tensorflow-serving/README.html)

## Pull and start the Intel® Extension for TensorFlow\* Serving CPU Docker container

```bash
docker pull intel/intel-extension-for-tensorflow:serving-cpu
docker run -it -p 8500:8500 -e MODEL_NAME=<your-model-name> -e MODEL_DIR=<your-model-dir> intel/intel-extension-for-tensorflow:serving-cpu
```

Then go to your browser on http://localhost:8888/.

For further information, please check the [Intel® Extension for TensorFlow](https://github.com/intel/intel-extension-for-tensorflow) GitHub.

**LEGAL NOTICE: By accessing, downloading or using this software and any required dependent software (the “Software Package”), you agree to the terms and conditions of the software license agreements for the Software Package, which may also include notices, disclaimers, or license terms for third party software included with the Software Package. Please refer to the “third-party-programs.txt” or other similarly-named text file for additional details.**

## Tag Descriptions

| Tag(s)                     | Intel® Extension for TensorFlow\* Version | TensorFlow Version | Driver Version | Container OS | Comments |
| :---:                      | :----:   | :---:    | :---:         | :---:    | :---                                                            |
| latest<br/>xpu<br/>2.14.0.1-xpu<br/> | 2.14.0.1    | 2.14.1   | [736](https://dgpu-docs.intel.com/releases/stable_736_25_20231031.html) | Ubuntu\* 22.04 | Intel® Extension for TensorFlow\* version 2.14.0.1 with Intel® Data Center Flex Series GPU, Intel® Data Center Max Series GPU, and Intel® Optimization for Horovod* support |
| cpu<br/>2.14.0.1-cpu           | 2.14.0.1    | 2.14.1   | N/A | Ubuntu\* 22.04 | Intel® Extension for TensorFlow\* version 2.14.0.1 with CPU and Intel® Optimization for Horovod* support |
| 2.13.0.0-xpu | 2.13.0.0    | 2.13.0   | [647](https://dgpu-docs.intel.com/releases/stable_647_21_20230714.html) | Ubuntu\* 22.04 | Intel® Extension for TensorFlow\* version 2.13.0.0 with Intel® Data Center Flex Series GPU, Intel® Data Center Max Series GPU, and Intel® Optimization for Horovod* support |
| 2.13.0.0-cpu           | 2.13.0.0    | 2.13.0   | N/A | Ubuntu\* 20.04 | Intel® Extension for TensorFlow\* version 2.13.0.0 with CPU and Intel® Optimization for Horovod* support |
| gpu<br/>1.2.0-gpu<br/> | 1.2.0    | 2.12.0   | [stable_602_20230323](https://dgpu-docs.intel.com/releases/stable_602_20230323.html) | Ubuntu\* 22.04 | Intel® Extension for TensorFlow\* version 1.2.0 with Intel® Data Center Flex Series GPU and Intel® Data Center Max Series GPU support |
| gpu-horovod<br/>1.2.0-gpu-horovod | 1.2.0    | 2.12.0   | [stable_602_20230323](https://dgpu-docs.intel.com/releases/stable_602_20230323.html) | Ubuntu\* 22.04 | Intel® Extension for TensorFlow\* version 1.2.0 with Intel® Data Center Flex Series GPU, Intel® Data Center Max Series GPU, and Intel® Optimization for Horovod* support |
| 1.2.0-cpu           | 1.2.0    | 2.12.0   | N/A | Ubuntu\* 20.04 | Intel® Extension for TensorFlow\* version 1.2.0 with CPU support |
| 1.1.0-gpu<br/>gpu-max<br/>1.1.0-gpu-max | 1.1.0    | 2.11.0   | [stable_540_20221205](https://dgpu-docs.intel.com/releases/stable_540_20221205.html) | Ubuntu\* 22.04 | Intel® Extension for TensorFlow\* version 1.1.0 with Intel® Data Center Max Series GPU support |
| gpu-flex<br/>1.1.0-gpu-flex | 1.1.0    | 2.11.0   | [stable_540_20221205](https://dgpu-docs.intel.com/releases/stable_540_20221205.html) | Ubuntu\* 22.04 | Intel® Extension for TensorFlow\* version 1.1.0 with Intel® Data Center GPU Flex Series support |
| 1.1.0-cpu           | 1.1.0    | 2.11.0   | N/A | Ubuntu\* 20.04 | Intel® Extension for TensorFlow\* version 1.1.0 with CPU support |
| 1.0.0-gpu                  | 1.0.0    | 2.10.0   | [stable_419_40_20220914](https://dgpu-docs.intel.com/releases/stable_419_40_20220914.html) | Ubuntu\* 20.04 | Intel® Extension for TensorFlow\* version 1.0.0 with Intel® Data Center GPU Flex Series support |
| 1.0.0-cpu                  | 1.0.0    | 2.10.0   | N/A | Ubuntu\* 20.04 | Intel® Extension for TensorFlow\* version 1.0.0 with CPU support |
| source                     | N/A      | N/A      | N/A | Ubuntu\* 20.04 | Intel® Extension for TensorFlow\* source docker image            |

| Tag(s)                     | Intel® Extension for TensorFlow\* Version | TensorFlow Serving Version | Driver Version | Container OS | Comments |
| :---:                      | :----:   | :---:    | :---:         | :---:    | :---                                                            |
| serving-gpu<br/>2.14.0.1-serving-gpu | 2.14.0.1    | 2.14.1   | [736](https://dgpu-docs.intel.com/releases/stable_736_25_20231031.html) | Ubuntu\* 22.04 | Intel® Extension for TensorFlow\* version 2.14.0.1 with Intel® Data Center Flex Series GPU, Intel® Data Center Max Series GPU and Tensorflow* Serving support|
| serving-cpu<br/>2.14.0.1-serving-cpu | 2.14.0.1   | 2.14.1   | N/A | Ubuntu\* 22.04 | Intel® Extension for TensorFlow\* version 2.14.0.1 with CPU and Tensorflow* Serving support |
| 2.13.0.0-serving-gpu | 2.13.0.0    | 2.13.0   | [647](https://dgpu-docs.intel.com/releases/stable_647_21_20230714.html) | Ubuntu\* 22.04 | Intel® Extension for TensorFlow\* version 2.13.0.0 with Intel® Data Center Flex Series GPU, Intel® Data Center Max Series GPU and Tensorflow* Serving support|
| 2.13.0.0-serving-cpu | 2.13.0.0   | 2.13.0   | N/A | Ubuntu\* 22.04 | Intel® Extension for TensorFlow\* version 2.13.0.0 with CPU and Tensorflow* Serving support |

- Other names and brands may be claimed as the property of others.
