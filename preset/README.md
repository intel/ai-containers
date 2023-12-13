# Intel® AI Tools Selector Preset Containers
Intel® AI Tools Selector Preset Containers provides data scientists and developers with environment to perform various data-science tasks such as data analysis, data processing, machine learning and deep learning models training and inference. Each container is equipped with the Python packages and tools suited for each tasks while being powered by Intel® Distribution For Python. More detail about each container is described in the table below.

## Preset Containers

| Preset Container Name | Purpose | Tools | Image Name |
| -----------------------------| ------------- | ------------- | ----------------- |
| Data Analytics | Perform large scale data analysis | [Intel® Distribution For Python](https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-for-python.html), [Modin*](https://github.com/modin-project/modin), [Intel® Dataset Librarian](https://github.com/IntelAI/models/tree/master/datasets/dataset_api), [Intel® Data Connector](https://github.com/IntelAI/models/tree/master/datasets/cloud_data_connector) | [`intel/data-analytics:latest-py3.9`](https://hub.docker.com/r/intel/data-analytics/tags)<br />[`intel/data-analytics:latest-py3.10`](https://hub.docker.com/r/intel/data-analytics/tags) |
| Classical ML | Train classical-ml models using scikit, modin and xgboost | [Intel® Distribution For Python](https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-for-python.html), [Intel® extension for SciKit Learn](https://github.com/intel/scikit-learn-intelex), [XGBoost*](https://github.com/dmlc/xgboost), [Modin*](https://github.com/modin-project/modin), <br /> [Intel® Dataset Librarian](https://github.com/IntelAI/models/tree/master/datasets/dataset_api), [Intel® Data Connector](https://github.com/IntelAI/models/tree/master/datasets/cloud_data_connector) | [`intel/classical-ml:latest-py3.9`](https://hub.docker.com/r/intel/classical-ml/tags)<br />[`intel/classical-ml:latest-py3.10`](https://hub.docker.com/r/intel/classical-ml/tags) |
| Deep Learning | Train large scale Deep Learning models with Tensorflow or PyTorch | [Intel® Distribution For Python](https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-for-python.html), [PyTorch*](https://pytorch.org/), [Tensorflow*](https://www.tensorflow.org/),<br /> [Intel® Extension for PyTorch](https://github.com/intel/intel-extension-for-pytorch), [Intel® Extension for Tensorflow](https://github.com/intel/intel-extension-for-tensorflow),<br /> [Intel® Optimization for Horovod](https://github.com/intel/intel-optimization-for-horovod), [Intel® Dataset Librarian](https://github.com/IntelAI/models/tree/master/datasets/dataset_api), [Intel® Data Connector](https://github.com/IntelAI/models/tree/master/datasets/cloud_data_connector), [Intel® Extension for DeepSpeed](https://github.com/intel/intel-extension-for-deepspeed) | [`intel/deep-learning:latest-py3.9`](https://hub.docker.com/r/intel/deep-learning/tags)<br />[`intel/deep-learning:latest-py3.10`](https://hub.docker.com/r/intel/deep-learning/tags) |
| Inference Optimization | Optimize Deep Learning models for inference<br /> using Intel® Neural Compressor | [Intel® Distribution For Python](https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-for-python.html), [PyTorch*](https://pytorch.org/), [Tensorflow*](https://www.tensorflow.org/), <br /> [Intel® Extension for PyTorch](https://github.com/intel/intel-extension-for-pytorch), [Intel® Extension for Tensorflow](https://github.com/intel/intel-extension-for-tensorflow),<br /> [Intel® Neural Compressor](https://github.com/intel/neural-compressor), [Intel® Dataset Librarian](https://github.com/IntelAI/models/tree/master/datasets/dataset_api), [Intel® Data Connector](https://github.com/IntelAI/models/tree/master/datasets/cloud_data_connector) | [`intel/inference-optimization:latest-py3.9`](https://hub.docker.com/r/intel/inference-optimization/tags)<br />[`intel/inference-optimization:latest-py3.10`](https://hub.docker.com/r/intel/inference-optimization/tags) |

## Prerequisites

1. Make sure [docker](https://docs.docker.com/engine/) is installed on the machine. Follow the [instruction here](https://docs.docker.com/engine/install/) to install docker engine on a host machine.

2. Pull a Preset Container of your choice from the [Intel® AI Tools Selector](https://www.intel.com/content/www/us/en/developer/tools/oneapi/ai-tools-selector.html) or from the [table](#preset-containers). The commands below use the `deep-learning` preset as an example.

```bash
docker pull intel/deep-learning:latest-py3.9
```

## Run Preset Container
There are 3 modes to run these containers:

* [Interactive](#run-in-interactive-mode)
* [Jupyter](#run-using-jupyter-notebook)
* [Multi-Node Distributed Training](#run-in-multi-node-distributed-mode-advanced) (Deep Learning and Inference Optimization)

>**Note:** Modify the commands below to fit your use case, especially the image, environment variables, and GPU device path.

### Run in Interactive Mode
This mode allows running the container in an interactive shell. This enables the ability to interact with the container's bash shell. Below is the command to start the container in interactive mode:

#### Run on CPU

```bash
docker run -it --rm \
    --shm-size=12G \
    -v ${PWD}:/home/dev/workdir \
    intel/deep-learning:latest-py3.9 bash
```

>**Note:** Certain applications use shared memory to share data between processes. But the default shared memory segment size is 64M for docker containers, and is not enough for multithreaded applications(Ex. Modin). Docker recommends increasing shared memory size using `--shm-size`.


#### Run on GPU
Find your machine's `RENDER` and `VIDEO` group values to enable [Intel® Flex/Max GPU](https://www.intel.com/content/www/us/en/products/details/discrete-gpus/data-center-gpu.html).

```bash
RENDER=$(getent group render | sed -E 's,^render:[^:]*:([^:]*):.*$,\1,')
VIDEO=$(getent group video | sed -E 's,^video:[^:]*:([^:]*):.*$,\1,')
test -z "$RENDER" || RENDER_GROUP="--group-add ${RENDER}"
test -z "$VIDEO" || VIDEO_GROUP="--group-add ${VIDEO}"
```

```bash
docker run -it --rm \
    ${RENDER_GROUP} \
    ${VIDEO_GROUP} \
    --device=/dev/dri \
    --shm-size=12G \
    -v ${PWD}:/home/dev/workdir \
    -v /dev/dri/by-path:/dev/dri/by-path \
    intel/deep-learning:latest-py3.9 bash
```

>**Note:** Certain applications use shared memory to share data between processes. But the default shared memory segment size is 64M for docker containers, and is not enough for multithreaded applications(Ex. Modin). Docker recommends increasing shared memory size using `--shm-size`.


#### Next Steps

1. For Deep Learning and Inference Optimization containers there will be separate conda environments for each AI framework: `pytorch-cpu`, `pytorch-gpu` and `tensorflow`. Use the command below to activate one environment:

```bash
conda activate <env-name>
```

2. Select a test from the `sample-tests` folder and run it using the following command as an example:

```bash
bash sample-tests/onnx/run.sh
# or if no bash script is found
python sample-tests/intel_extension_for_tensorflow/test_itex.py
```

### Run using Jupyter Notebook
This mode launches a jupyterlab notebook server. The command below will start the jupyterlab server which can be accessed from a web browser. Each container includes jupyter kernel to enable conda environment in jupyter notebook. The port for this server is `8888` and is exposed by default when you run the container.

>**Note:** When launching a jupyter notebook server this way, docker assigns a [network](https://docs.docker.com/engine/tutorials/networkingcontainers/) such that the container can communicate with other applications like a web browser. By default docker launches containers with the `bridge` network, but if you are trying to access this server from a machine you are `ssh`'ing into, change the network mode with the `--net=host` flag and ensure you are local port forwarding with `ssh -L 8888:8888`.

#### Run on CPU

```bash
docker run -it --rm \
    --shm-size=12G \
    -v ${PWD}:/home/dev/workdir \
    intel/deep-learning:latest-py3.9
```

>**Note:** Certain applications use shared memory to share data between processes. But the default shared memory segment size is 64M for docker containers, and is not enough for multithreaded applications(Ex. Modin). Docker recommends increasing shared memory size using `--shm-size`.

#### Run on GPU
Find your machine's `RENDER` and `VIDEO` group values to enable [Intel® Flex/Max GPU](https://www.intel.com/content/www/us/en/products/details/discrete-gpus/data-center-gpu.html).

```bash
RENDER=$(getent group render | sed -E 's,^render:[^:]*:([^:]*):.*$,\1,')
VIDEO=$(getent group video | sed -E 's,^video:[^:]*:([^:]*):.*$,\1,')
test -z "$RENDER" || RENDER_GROUP="--group-add ${RENDER}"
test -z "$VIDEO" || VIDEO_GROUP="--group-add ${VIDEO}"
```

```bash
docker run -it --rm \
    ${RENDER_GROUP} \
    ${VIDEO_GROUP} \
    --device=/dev/dri \
    --shm-size=12G \
    -v ${PWD}:/home/dev/workdir \
    -v /dev/dri/by-path:/dev/dri/by-path \
    intel/deep-learning:latest-py3.9
```

>**Note:** Certain applications use shared memory to share data between processes. But the default shared memory segment size is 64M for docker containers, and is not enough for multithreaded applications(Ex. Modin). Docker recommends increasing shared memory size using `--shm-size`.

#### Next Steps

1. After running this command the terminal should display an output similar to displayed below in the image ![image](https://github.com/intel/ai-containers/assets/18349036/0a8a2d05-f7b0-4a9f-994e-bcc4e4b703a0) The server address together with the port set can be used to connect to the jupyter server in a web browser. For example `http://127.0.0.1:8888`. The token displayed after the `token=` can be used as a password to login into the server. For example in the image displayed above the token is `b66e74a85bc2570bf15782e5124c933c3a4ddabd2cf2d7d3`.

2. Select a notebook sample from the Overview notebook found in directory you launched the server with. In this example, the `intel/deep-learning` container has a notebook titled [`Deep_Learning_Samples_Overview.ipynb`](./deep-learning/notebooks/deep-learning/Deep_Learning_Samples_Overview.ipynb) when launched in jupyter mode.

3. After selecting a notebook sample, select the preset kernel found in the dropdown menu presented when loading the notebook. For Deep Learning and Inference Optimization containers there will be multiple kernels, one for each framework: `pytorch`, `pytorch-gpu`, and `tensorflow`.

##### Advanced Jupyter Server Configuration

Modify your notebook server command by using the default example below to change the network (port/ip) and security (privilege) settings by appending it to the docker run commands above:

```bash
docker run ... intel/deep-learning:latest-py3.9 \
    bash -c "jupyter notebook --notebook-dir=~/jupyter \
            --port 8888 \
            --ip 0.0.0.0 \
            --no-browser \
            --allow-root"
```

## Run in Multi-Node Distributed Mode [Advanced]

You can follow the instructions provided for [Tensorflow](./deep-learning/demo/tensorflow-distributed/README.md) and [PyTorch](./deep-learning/demo/pytorch-distributed/README.md) along with the Deep Learning or Inference Optimization presets using your preferred framework.

## Troubleshooting and Support
If you face some issue in using the container you can find more information on how to troubleshoot [here](https://github.com/intel/ai-containers#troubleshooting). If you need more help feel free to submit an [issue](https://github.com/intel/ai-containers/issues).

---

* Other names and brands may be claimed as the property of others. [Trademarks](http://www.intel.com/content/www/us/en/legal/trademarks.html)
