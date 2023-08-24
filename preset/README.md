# Intel® Web Configurator Preset Containers
Intel® Web Configurator Preset Containers provides data scientists and developers with environment to perform various data-science tasks such as data analysis, data processing, machine learning and deep learning models training and inference. Each container is equipped with the Python packages and tools suited for each tasks while being powered by Intel® Distribution For Python. More detail about each container is described in the table below.

## Preset Containers

| Preset Container Name | Purpose | Tools | Image Name |
| -----------------------------| ------------- | ------------- | ----------------- |
| Data Analytics | Perform large scale data analysis | [Intel® Distribution For Python](https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-for-python.html), [Modin](https://github.com/modin-project/modin), [Intel® Dataset Librarian](https://github.com/IntelAI/models/tree/master/datasets/dataset_api), [Intel® Data Connector](https://github.com/IntelAI/models/tree/master/datasets/cloud_data_connector) | `intel/data-analytics:2023.2-py3.9`<br />`intel/data-analytics:2023.2-py3.10` |
| Classical ML | Train classical-ml models using scikit, modin and xgboost | [Intel® Distribution For Python](https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-for-python.html), [Intel® extension for SciKit Learn](https://github.com/intel/scikit-learn-intelex), [XGBoost](https://github.com/dmlc/xgboost), [Modin](https://github.com/modin-project/modin), <br /> [Intel® Dataset Librarian](https://github.com/IntelAI/models/tree/master/datasets/dataset_api), [Intel® Data Connector](https://github.com/IntelAI/models/tree/master/datasets/cloud_data_connector) | `intel/classical-ml:2023.2-py3.9`<br />`intel/classical-ml:2023.2-py3.10` |
| Deep Learning | Train large scale Deep Learning models with Tensorflow or PyTorch | [Intel® Distribution For Python](https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-for-python.html), [PyTorch](https://pytorch.org/), [Tensorflow](https://www.tensorflow.org/),<br /> [Intel® Extension for PyTorch](https://github.com/intel/intel-extension-for-pytorch), [Intel® Extension for Tensorflow](https://github.com/intel/intel-extension-for-tensorflow),<br /> [Intel® Optimization for Horovod](https://github.com/intel/intel-optimization-for-horovod), [Intel® Dataset Librarian](https://github.com/IntelAI/models/tree/master/datasets/dataset_api), [Intel® Data Connector](https://github.com/IntelAI/models/tree/master/datasets/cloud_data_connector), [Intel® Extension for DeepSpeed*](https://github.com/intel/intel-extension-for-deepspeed) | `intel/deep-learning:2023.2-py3.9`<br />`intel/deep-learning:2023.2-py3.10` |
| Inference Optimization | Optimize Deep Learning models for inference<br /> using Intel® Neural Compressor | [Intel® Distribution For Python](https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-for-python.html), [PyTorch](https://pytorch.org/), [Tensorflow](https://www.tensorflow.org/), <br /> [Intel® Extension for PyTorch](https://github.com/intel/intel-extension-for-pytorch), [Intel® Extension for Tensorflow](https://github.com/intel/intel-extension-for-tensorflow),<br /> [Intel® Neural Compressor](https://github.com/intel/neural-compressor), [Intel® Dataset Librarian](https://github.com/IntelAI/models/tree/master/datasets/dataset_api), [Intel® Data Connector](https://github.com/IntelAI/models/tree/master/datasets/cloud_data_connector) | `intel/inference-optimization:2023.2-py3.9`<br />`intel/inference-optimization:2023.2-py3.10` |

The Deep Learning and Inference Optimization containers have separate conda environments for each framework: `torch` and `tensorflow`.

## Prerequisites
Make sure [docker](https://docs.docker.com/engine/) is installed on the machine. Follow the [instruction here](https://docs.docker.com/engine/install/) to install docker engine on a host machine.

## Clone the oneAPI Samples
It is recommended to have [oneAPI samples](https://github.com/oneapi-src/oneAPI-samples) repository cloned prior to running these containers.
For these containers, use the [Intel® AI Analytics Toolkit](https://github.com/oneapi-src/oneAPI-samples/tree/master/AI-and-Analytics) examples.

```bash
git clone --single-branch --branch=2023.2_AIKit https://github.com/oneapi-src/oneAPI-samples.git
cd oneAPI-samples/AI-and-Analytics
```
Since the container runs as non root user, it is advised to give correct permissions to files and folders under `AI-and-Analytics` folder.

To not expose samples into the container, simply remove `-v ${PWD}:/home/dev/jupyter` from `docker run` commands below.

In addition to the examples, any files in the working directory will be exposed in the container. For more information about exposing, see [Volumes](https://docs.docker.com/storage/volumes/).
In order to do so, add the following option to any of the `docker run` commands below:
```bash
-v /absolute/path/to/examples/dir:/home/dev/jupyter/<my_samples>
```
Once the container is ready, your can find your examples under `my_samples` directory.

## Run Preset Container
There are 2 modes to run thess containers:

* Interactive
* Jupyter

Before starting, pick the name of the container image from the [table](#preset-containers) based on the task to perform.

#### Run in Interactive Mode
This mode allows running the container in an interactive shell. This enables the ability to interact with the container's bash shell. Below is the command to start the container in interactive mode:

Please note that certain applications use shared memory to share data between processes. But the default shared memory segment size is 64M for container, and is not enough for multithreaded applications(Ex. Modin). Docker recommends increasing shared memory size using --shm-size command line options provided at runtime to `docker run` command. Please, modify shared memory segment size in the following format according to need: --shm-size=256M or --shm-size=4G for example as a command line option like so: `docker run --shm-size=4G`.

```bash
docker run -it --rm -v ${PWD}:/home/dev/jupyter <image name> bash
```
or if you plan to exapose your own samples directory into the container as well:
```bash
docker run -it --rm \
    -v ${PWD}:/home/dev/jupyter \
    -v <path_to_your_examples_directory>:/home/dev/jupyter/<my_samples> \
    <image name> bash
```

If you want to enable [Intel® Flex/Max GPU](https://www.intel.com/content/www/us/en/products/details/discrete-gpus/data-center-gpu.html) optimization, please use the following command. Please note that test for the `render` group sets the Group ID for the GPU device to enable GPU optimization inside the container.

```bash
RENDER=$(getent group render | sed -E 's,^render:[^:]*:([^:]*):.*$,\1,')
test -z "$RENDER" || RENDER_GROUP="--group-add ${RENDER}"

docker run -it --rm \
    ${RENDER_GROUP} \
    --device=/dev/dri \
    -v ${PWD}:/home/dev/jupyter \
    -v /dev/dri/by-path:/dev/dri/by-path \
    <image name> bash
```

### Run using Jupyter Notebook
This mode launches a jupyterlab notebook server. The command below will start the jupyterlab server which can be accessed from a web browser. Each container includes jupyter kernel to enable conda environemt in jupyter notebook. The Deep Learning and Inference Optimization containers include  `torch` and `tensorflow` kernels to separate environments for both frameworks.

```bash
export PORT=<port>
docker run -it --rm -e PORT=$PORT -p $PORT:$PORT -v ${PWD}:/home/dev/jupyter <image name>
```

If you want to enable [Intel® Flex/Max GPU](https://www.intel.com/content/www/us/en/products/details/discrete-gpus/data-center-gpu.html) optimization, please use the following command. Please note that test for the `render` group sets the Group ID for the GPU device to enable GPU optimization inside the container.

```bash
export PORT=<port>
RENDER=$(getent group render | sed -E 's,^render:[^:]*:([^:]*):.*$,\1,')
test -z "$RENDER" || RENDER_GROUP="--group-add ${RENDER}"

docker run -it --rm -e PORT=$PORT \
    ${RENDER_GROUP} \
    --device=/dev/dri \
    -v ${PWD}:/home/dev/jupyter \
    -v /dev/dri/by-path:/dev/dri/by-path \
    -p $PORT:$PORT \
    <image name>
```

After running this command the terminal should display an output similar to displayed below in the image ![image](https://github.com/intel/ai-containers/assets/18349036/0a8a2d05-f7b0-4a9f-994e-bcc4e4b703a0) The server address together with the port set can be used to connect to the jupyter server in a web browser. For example `http://127.0.0.1:8888`. The token displayed after the `token=` can be used as a password to login into the server. For example in the image displayed above the token is `b66e74a85bc2570bf15782e5124c933c3a4ddabd2cf2d7d3`.

## Troubleshooting and Support
If you face some issue in using the container you can find more information on how to troubleshoot [here](https://github.com/intel/ai-containers#troubleshooting). If you need more help feel free to submit an [issue](https://github.com/intel/ai-containers/issues).
