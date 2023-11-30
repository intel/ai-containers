# Intel® AI Tools Selector Preset Containers
Intel® AI Tools Selector Preset Containers provides data scientists and developers with environment to perform various data-science tasks such as data analysis, data processing, machine learning and deep learning models training and inference. Each container is equipped with the Python packages and tools suited for each tasks while being powered by Intel® Distribution For Python. More detail about each container is described in the table below.

You can get the Preset Containers from [Intel® AI Tools Selector](https://www.intel.com/content/www/us/en/developer/tools/oneapi/ai-tools-selector.html).

## Preset Containers

| Preset Container Name | Purpose | Tools | Image Name |
| -----------------------------| ------------- | ------------- | ----------------- |
| Data Analytics | Perform large scale data analysis | [Intel® Distribution For Python](https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-for-python.html), [Modin*](https://github.com/modin-project/modin), [Intel® Dataset Librarian](https://github.com/IntelAI/models/tree/master/datasets/dataset_api), [Intel® Data Connector](https://github.com/IntelAI/models/tree/master/datasets/cloud_data_connector) | `intel/data-analytics:latest-py3.9`<br />`intel/data-analytics:latest-py3.10` |
| Classical ML | Train classical-ml models using scikit, modin and xgboost | [Intel® Distribution For Python](https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-for-python.html), [Intel® extension for SciKit Learn](https://github.com/intel/scikit-learn-intelex), [XGBoost*](https://github.com/dmlc/xgboost), [Modin*](https://github.com/modin-project/modin), <br /> [Intel® Dataset Librarian](https://github.com/IntelAI/models/tree/master/datasets/dataset_api), [Intel® Data Connector](https://github.com/IntelAI/models/tree/master/datasets/cloud_data_connector) | `intel/classical-ml:latest-py3.9`<br />`intel/classical-ml:latest-py3.10` |
| Deep Learning | Train large scale Deep Learning models with Tensorflow or PyTorch | [Intel® Distribution For Python](https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-for-python.html), [PyTorch*](https://pytorch.org/), [Tensorflow*](https://www.tensorflow.org/),<br /> [Intel® Extension for PyTorch](https://github.com/intel/intel-extension-for-pytorch), [Intel® Extension for Tensorflow](https://github.com/intel/intel-extension-for-tensorflow),<br /> [Intel® Optimization for Horovod](https://github.com/intel/intel-optimization-for-horovod), [Intel® Dataset Librarian](https://github.com/IntelAI/models/tree/master/datasets/dataset_api), [Intel® Data Connector](https://github.com/IntelAI/models/tree/master/datasets/cloud_data_connector), [Intel® Extension for DeepSpeed](https://github.com/intel/intel-extension-for-deepspeed) | `intel/deep-learning:latest-py3.9`<br />`intel/deep-learning:latest-py3.10` |
| Inference Optimization | Optimize Deep Learning models for inference<br /> using Intel® Neural Compressor | [Intel® Distribution For Python](https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-for-python.html), [PyTorch*](https://pytorch.org/), [Tensorflow*](https://www.tensorflow.org/), <br /> [Intel® Extension for PyTorch](https://github.com/intel/intel-extension-for-pytorch), [Intel® Extension for Tensorflow](https://github.com/intel/intel-extension-for-tensorflow),<br /> [Intel® Neural Compressor](https://github.com/intel/neural-compressor), [Intel® Dataset Librarian](https://github.com/IntelAI/models/tree/master/datasets/dataset_api), [Intel® Data Connector](https://github.com/IntelAI/models/tree/master/datasets/cloud_data_connector) | `intel/inference-optimization:latest-py3.9`<br />`intel/inference-optimization:latest-py3.10` |

The Deep Learning and Inference Optimization containers have separate conda environments for each framework: `pytorch-cpu`, `pytorch-gpu` and `tensorflow-xpu`.

## Prerequisites
Make sure [docker](https://docs.docker.com/engine/) is installed on the machine. Follow the [instruction here](https://docs.docker.com/engine/install/) to install docker engine on a host machine.

Find your machine's `RENDER` and `VIDEO` group values to enable [Intel® Flex/Max GPU](https://www.intel.com/content/www/us/en/products/details/discrete-gpus/data-center-gpu.html).
```bash
RENDER=$(getent group render | sed -E 's,^render:[^:]*:([^:]*):.*$,\1,')
VIDEO=$(getent group video | sed -E 's,^video:[^:]*:([^:]*):.*$,\1,')
test -z "$RENDER" || RENDER_GROUP="--group-add ${RENDER}"
test -z "$VIDEO" || VIDEO_GROUP="--group-add ${VIDEO}"
```

## Run Preset Container
There are 2 modes to run thess containers:

* Interactive
* Jupyter

Before starting, pick the name of the container image from the [table](#preset-containers) based on the task to perform. The commands below use `intel/deep-learning:latest-py3.9` as an example.

### Run in Interactive Mode
This mode allows running the container in an interactive shell. This enables the ability to interact with the container's bash shell. Below is the command to start the container in interactive mode:

```bash
docker run -it --rm \
    ${RENDER_GROUP} \
    ${VIDEO_GROUP} \
    --shm-size=12G \
    -v ${PWD}:/home/dev/workdir \
    -w /home/dev/workdir \
    intel/deep-learning:latest-py3.9 bash
```

>**Note:** `${RENDER_GROUP}` and `${VIDEO_GROUP}` are required for utilizing Intel® Extension for PyTorch from the `torch` conda environment on both CPU and GPU.
>**Note:** Certain applications use shared memory to share data between processes. But the default shared memory segment size is 64M for docker containers, and is not enough for multithreaded applications(Ex. Modin). Docker recommends increasing shared memory size using `--shm-size`.

To utilize [Intel® Flex/Max GPU](https://www.intel.com/content/www/us/en/products/details/discrete-gpus/) optimizations, use the command below:

```bash
docker run -it --rm \
    ${RENDER_GROUP} \
    ${VIDEO_GROUP} \
    --device=/dev/dri \
    --shm-size=12G \
    -v ${PWD}:/home/dev/workdir \
    -v /dev/dri/by-path:/dev/dri/by-path \
    -w /home/dev/workdir \
    intel/deep-learning:latest-py3.9 bash
```

### Run using Jupyter Notebook
This mode launches a jupyterlab notebook server. The command below will start the jupyterlab server which can be accessed from a web browser. Each container includes jupyter kernel to enable conda environment in jupyter notebook.

```bash
export PORT=8888
```

```bash
docker run -it --rm \
    ${VIDEO_GROUP} \
    ${RENDER_GROUP} \
    -e PORT=$PORT \
    -p $PORT:$PORT \
    intel/deep-learning:latest-py3.9
```

If you want to enable [Intel® Flex/Max GPU](https://www.intel.com/content/www/us/en/products/details/discrete-gpus/data-center-gpu.html) optimization, please use the following command. Please note that test for the `render` group sets the Group ID for the GPU device to enable GPU optimization inside the container.

```bash
docker run -it --rm -e PORT=$PORT \
    ${VIDEO_GROUP} \
    ${RENDER_GROUP} \
    --device=/dev/dri \
    -v ${PWD}:/home/dev/jupyter \
    -v /dev/dri/by-path:/dev/dri/by-path \
    -p $PORT:$PORT \
    intel/deep-learning:latest-py3.9
```

After running this command the terminal should display an output similar to displayed below in the image ![image](https://github.com/intel/ai-containers/assets/18349036/0a8a2d05-f7b0-4a9f-994e-bcc4e4b703a0) The server address together with the port set can be used to connect to the jupyter server in a web browser. For example `http://127.0.0.1:8888`. The token displayed after the `token=` can be used as a password to login into the server. For example in the image displayed above the token is `b66e74a85bc2570bf15782e5124c933c3a4ddabd2cf2d7d3`.

## Run in Multi-Node Distributed Mode

You can follow the instructions provided in [Tensorflow README](./deep-learning/demo/tensorflow-distributed/README.md) and [PyTorch README](./deep-learning/demo/pytorch-distributed/README.md) along with the Deep Learning or Inference Optimization presets to run the preset containers in multi-node mode depending on your preferred framework.

## Troubleshooting and Support
If you face some issue in using the container you can find more information on how to troubleshoot [here](https://github.com/intel/ai-containers#troubleshooting). If you need more help feel free to submit an [issue](https://github.com/intel/ai-containers/issues).
*Other names and brands may be claimed as the property of others. [Trademarks](http://www.intel.com/content/www/us/en/legal/trademarks.html)
