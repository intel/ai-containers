# AI Tools Selector Preset Containers

AI Tools Selector Preset Containers provides data scientists and developers with environment to perform various data-science tasks such as data analysis, data processing, machine learning and deep learning models training and inference. Each container is equipped with the Python packages and tools suited for each task. More detail about each container is described in the table below.

## Preset Containers

| Preset Container Name | Purpose | Tools | Image Name |
| -----------------------------| ------------- | ------------- | ----------------- |
| Classical ML | Accelerate your machine learning and data science pipelines with the power of open libraries optimized for Intel® architectures |[Intel® extension for SciKit Learn](https://github.com/intel/scikit-learn-intelex),<br /> [Intel® Optimization for XGBoost*](https://github.com/dmlc/xgboost),<br /> [Modin*](https://github.com/modin-project/modin) | [`intel/classical-ml:latest-py3.11`](https://hub.docker.com/r/intel/classical-ml/tags) |
| Deep Learning PyTorch CPU | Boost the performance of your workloads, reduce model size, and improve the speed of your Deep Learning deployments on Intel® Xeon® processors with Intel® Extension for PyTorch* | [Intel® Extension for PyTorch](https://github.com/intel/intel-extension-for-pytorch), <br /> [Intel® Neural Compressor](https://github.com/intel/neural-compressor),<br /> [ONNX Runtime*](https://github.com/microsoft/onnxruntime) | [`intel/deep-learning:pytorch-latest-py3.11`](https://hub.docker.com/r/intel/deep-learning/tags) |
| Deep Learning PyTorch GPU | Boost the performance of your workloads, reduce model size, and improve the speed of your Deep Learning deployments on Intel® Data Center GPU Max Series with Intel® Extension for PyTorch* | [Intel® Extension for PyTorch](https://github.com/intel/intel-extension-for-pytorch), <br /> [Intel® Neural Compressor](https://github.com/intel/neural-compressor), <br /> [DeepSpeed*](https://github.com/microsoft/DeepSpeed)  | [`intel/deep-learning:pytorch-gpu-latest-py3.11`](https://hub.docker.com/r/intel/deep-learning/tags) |
| Deep Learning TensorFlow CPU| Boost the performance of your workloads, reduce model size, and improve the speed of your Deep Learning deployments on Intel® Xeon® processors with Intel® Extension for TensorFlow* | [Intel® Extension for Tensorflow](https://github.com/intel/intel-extension-for-tensorflow),<br /> [Intel® Neural Compressor](https://github.com/intel/neural-compressor),<br /> [ONNX Runtime*](https://github.com/microsoft/onnxruntime) | [`intel/deep-learning:tensorflow-latest-py3.11`](https://hub.docker.com/r/intel/deep-learning/tags) |
| Deep Learning TensorFlow GPU| Boost the performance of your workloads, reduce model size, and improve the speed of your Deep Learning deployments on Intel® Data Center GPU Max Series with Intel® Extension for TensorFlow* | [Intel® Extension for Tensorflow](https://github.com/intel/intel-extension-for-tensorflow),<br /> [Intel® Optimization for Horovod](https://github.com/intel/intel-optimization-for-horovod),<br /> [Intel® Neural Compressor](https://github.com/intel/neural-compressor) | [`intel/deep-learning:tensorflow-gpu-latest-py3.11`](https://hub.docker.com/r/intel/deep-learning/tags) |
| Deep Learning for JAX| Reduce model size and improve the speed of your Deep Learning deployments on Intel® Xeon® processors with JAX* | [JAX*](https://github.com/jax-ml/jax),<br /> [Intel® Distribution of Python](https://github.com/IntelPython/) | [`intel/deep-learning:jax-latest-py3.11`](https://hub.docker.com/r/intel/deep-learning/tags) |

## Prerequisites

1. Make sure [docker](https://docs.docker.com/engine/) is installed on the machine. Follow the [instruction here](https://docs.docker.com/engine/install/) to install docker engine on a host machine.

2. Pull a Preset Container of your choice from the [AI Tools Selector](https://www.intel.com/content/www/us/en/developer/tools/oneapi/ai-tools-selector.html) or from the [table](#preset-containers). The commands below use the `deep-learning for PyTorch CPU` preset as an example.

```bash
docker pull intel/deep-learning:pytorch-latest-py311
```

## Run Preset Container

There are 3 modes to run these containers:

* [Jupyter](#run-using-jupyter-notebook)
* [Interactive](#run-in-interactive-mode)
* [Multi-Node Distributed Training](#run-in-multi-node-distributed-mode-advanced) (Deep Learning PyTorch GPU Deep Learning TensorFlow GPU)
)

> [!NOTE]
> Modify the commands below to fit your use case, especially the image, environment variables, and GPU device path.

### Run using Jupyter Notebook

This mode launches a jupyterlab notebook server. The command below will start the jupyterlab server which can be accessed from a web browser. Each container includes jupyter kernel to enable conda environment in jupyter notebook. The port for this server is `8888` and is exposed by default when you run the container.

> [!NOTE]
> When launching a jupyter notebook server this way, docker assigns a [network](https://docs.docker.com/engine/tutorials/networkingcontainers/) such that the container can communicate with other applications like a web browser. By default docker launches containers with the `bridge` network, but if you are trying to access this server from a machine you are `ssh`'ing into, change the network mode with the `--net=host` flag and ensure you are local port forwarding with `ssh -L 8888:8888`.

#### Run on Jupyter CPU

```bash
docker run -it --rm \
    -p 8888:8888 --shm-size=12G \
    -v ${PWD}:/home/dev/workdir \
    intel/deep-learning:pytorch-latest-py3.11
```

> [!NOTE]
> Certain applications use shared memory to share data between processes. But the default shared memory segment size is 64M for docker containers, and is not enough for multithreaded applications (Ex. Modin*). Docker recommends increasing shared memory size using `--shm-size`.

#### Run on Jupyter GPU

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
    -p 8888:8888  --shm-size=12G \
    -v ${PWD}:/home/dev/workdir \
    -v /dev/dri/by-path:/dev/dri/by-path \
    intel/deep-learning:pytorch-gpu-latest-py3.11
```

#### Next Steps

1. After running this command the terminal should display an output similar to displayed below in the image ![image](https://github.com/intel/ai-containers/assets/18349036/0a8a2d05-f7b0-4a9f-994e-bcc4e4b703a0) The server address together with the port set can be used to connect to the jupyter server in a web browser. For example `http://127.0.0.1:8888`. The token displayed after the `token=` can be used as a password to login into the server. For example in the image displayed above the token is `b66e74a85bc2570bf15782e5124c933c3a4ddabd2cf2d7d3`.

2. Select a notebook sample from the Overview notebook found in directory you launched the server with. In this example, the `intel/deep-learning:pytorch-latest-py3.11` container has a notebook titled [`Deep_Learning_Samples_Overview.ipynb`](https://github.com/intel/ai-containers/blob/main/preset/deep-learning-pytorch/notebooks/Deep_Learning_Samples_Overview.ipynb) when launched in jupyter mode.

3. After selecting a notebook sample, select the preset kernel found in the dropdown menu presented when loading the notebook. For each container there will be a kernel with the environment name: `classical-ml`, `jax`, `pytorch-cpu`, `pytorch-gpu` `tensorflow-cpu` and  `tensorflow-gpu`.

##### Advanced Jupyter Server Configuration

Modify your notebook server command by using the default example below to change the network (port/ip) and security (privilege) settings by appending it to the docker run commands above:

```bash
docker run ... intel/deep-learning:pytorch-latest-py3.11 \
    bash -c "jupyter notebook --notebook-dir=~/jupyter \
            --port 8888 \
            --ip 0.0.0.0 \
            --no-browser \
            --allow-root"
```

### Run in Interactive Mode

This mode allows running the container in an interactive shell. This enables the ability to interact with the container's bash shell. Below is the command to start the container in interactive mode:

#### Run on CPU

```bash
docker run -it --rm \
    -p 8888:8888 --shm-size=12G \
    -v ${PWD}:/home/dev/workdir \
    intel/deep-learning:pytorch-latest-py3.11 bash
```

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
    -p 8888:8888 --shm-size=12G \
    -v ${PWD}:/home/dev/workdir \
    -v /dev/dri/by-path:/dev/dri/by-path \
    intel/deep-learning:pytorch-latest-py3.11 bash
```

> [!NOTE]
> Certain applications use shared memory to share data between processes. But the default shared memory segment size is 64M for docker containers, and is not enough for multithreaded applications(Ex. Modin). Docker recommends increasing shared memory size using `--shm-size`.

#### Next Steps

1. For each container there will be a kernel with the environment name: `classical-ml`, `jax`, `pytorch-cpu`, `pytorch-gpu` `tensorflow-cpu` and  `tensorflow-gpu`. Use the command below to activate the `pytorch-cpu` environment in the Deep Learning PyTorch CPU preset:

    ```bash
    conda activate pytorch-cpu
    ```

2. Select a test from the `sample-tests` folder and run it using the following command as an example:

    ```bash
    python sample-tests/intel_extension_for_pytorch/test_ipex.py
    ```

    The `test_ipex.py` script utilizes PyTorch to classify images with a pre-trained ResNet-50 model.
    Users can specify whether to run the script on a CPU or XPU, and there is an option to apply optimizations using Intel Extension for PyTorch (IPEX).
    Transfers both the model and data to the chosen device, and then measures the average inference time over 100 runs, excluding the initial warm-up phase.
    Finally, the script prints the average inference time.

> [!NOTE]
> The `sample-tests` folder may differ in each container, and some tests use a bash script.

## Run in Multi-Node Distributed Mode [Advanced]

You can follow the instructions provided for [Intel® Extension for TensorFlow*](https://github.com/intel/ai-containers/tree/main/preset/deep-learning/demo/tensorflow-distributed/README.md) and [Intel® Extension for PyTorch*](https://github.com/intel/ai-containers/tree/main/preset/deep-learning/demo/pytorch-distributed/README.md) along with the Deep Learning PyTorch GPU or Deep Learning TensorFlow GPU presets using your preferred framework.

## Troubleshooting and Support

If you face some issue in using the container you can find more information on how to troubleshoot [here](https://github.com/intel/ai-containers#troubleshooting). If you need more help feel free to submit an [issue](https://github.com/intel/ai-containers/issues).

---

*Other names and brands may be claimed as the property of others. [Trademarks](http://www.intel.com/content/www/us/en/legal/trademarks.html)
