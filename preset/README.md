# AI Tools Preset Containers

AI Tools Preset Containers provide data scientists and developers with ready-to-use environments for tasks like data analysis, data processing, machine learning, and deep learning. Each container includes Python\* packages and tools tailored to specific tasks. More details are provided in the table below.

## Preset Containers

| Preset Container Name | Purpose | Tools | Image Name |
| -----------------------------| ------------- | ------------- | ----------------- |
| Deep Learning PyTorch\* CPU | Boost the performance of your workloads, reduce model size, and improve the speed of your Deep Learning deployments on Intel® Xeon® processors with Intel® Extension for PyTorch* | <li>[Intel® Extension for PyTorch](https://github.com/intel/intel-extension-for-pytorch), <br /> <li>[Intel® Neural Compressor](https://github.com/intel/neural-compressor),<br /> <li>[ONNX Runtime\*](https://github.com/microsoft/onnxruntime) | [`intel/deep-learning:pytorch-latest-py3.11`](https://hub.docker.com/r/intel/deep-learning/tags) |
| Deep Learning PyTorch\* GPU | Boost the performance of your workloads, reduce model size, and improve the speed of your Deep Learning deployments on Intel® Data Center GPU Max Series with Intel® Extension for PyTorch\* | <li>[Intel® Extension for PyTorch](https://github.com/intel/intel-extension-for-pytorch), <br /> <li>[Intel® Neural Compressor](https://github.com/intel/neural-compressor), <br /> <li>[DeepSpeed\*](https://github.com/microsoft/DeepSpeed)  | [`intel/deep-learning:pytorch-gpu-latest-py3.11`](https://hub.docker.com/r/intel/deep-learning/tags) |
| Deep Learning JAX\* CPU| Reduce model size and improve the speed of your Deep Learning deployments on Intel® Xeon® processors with JAX\* | <li>[JAX\*](https://github.com/jax-ml/jax) | [`intel/deep-learning:jax-latest-py3.11`](https://hub.docker.com/r/intel/deep-learning/tags) |

## Prerequisites

1. Make sure [Docker](https://docs.docker.com/engine/) is installed on the machine. Follow the [instruction here](https://docs.docker.com/engine/install/) to install docker engine on a host machine.

2. Pull a preset container of your choice from the [AI Tools Selector](https://www.intel.com/content/www/us/en/developer/tools/oneapi/ai-tools-selector.html) or from the [table](#preset-containers). The commands below use the `Deep Learning for PyTorch* CPU` preset as an example.

```bash
docker pull intel/deep-learning:pytorch-latest-py311
```

## Run Preset Container

There are three modes to run these containers:

* [Jupyter Notebook](#run-using-jupyter-notebook)
* [Interactive](#run-in-interactive-mode)
* [Multi-Node Distributed Training](#run-in-multi-node-distributed-mode-advanced) (Deep Learning PyTorch GPU)

> [!NOTE]
> Modify the commands below to fit your use case, including the image, environment variables, and GPU device path.

### Run using Jupyter Notebook

This mode starts a JupyterLab notebook server, accessible via a web browser. Each container includes a Jupyter kernel to enable the conda environment in the Jupyter notebook. The port for this server is `8888` and is exposed by default when you run the container.

> [!NOTE]
> When launching a Jupyter notebook server this way, Docker assigns a [network](https://docs.docker.com/engine/tutorials/networkingcontainers/) that allows the container to communicate with other applications, such as a web browser. By default, Docker uses the `bridge` network. If you are trying to access this server from a remote machine via SSH, change the network mode with the `--net=host` flag and enable local port forwarding with `ssh -L 8888:8888`.

#### Run on Jupyter CPU

```bash
docker run -it --rm \
    -p 8888:8888 --shm-size=12G \
    -v ${PWD}:/home/dev/workdir \
    intel/deep-learning:pytorch-latest-py3.11
```

> [!NOTE]
> Some applications use shared memory to share data between processes. The default shared memory segment size for Docker containers is 64MB, which may be insufficient for multithreaded applications. Increase the shared memory size using `--shm-size`.

#### Run on Jupyter GPU

Identify your system's `RENDER` and `VIDEO` group values to enable [Intel® Data Center GPU Flex/Max Series](https://www.intel.com/content/www/us/en/products/details/discrete-gpus/data-center-gpu.html):

```bash
RENDER=$(getent group render | sed -E 's,^render:[^:]*:([^:]*):.*$,\1,')
VIDEO=$(getent group video | sed -E 's,^video:[^:]*:([^:]*):.*$,\1,')
test -z "$RENDER" || RENDER_GROUP="--group-add ${RENDER}"
test -z "$VIDEO" || VIDEO_GROUP="--group-add ${VIDEO}"
```

Run the container:

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

1. After running the command, the terminal should display output similar to the image below ![image](https://github.com/intel/ai-containers/assets/18349036/0a8a2d05-f7b0-4a9f-994e-bcc4e4b703a0). Use the displayed server address and port (for example, `http://127.0.0.1:8888`) to connect to the Jupyter server in a web browser. The token displayed after `token=` can be used as a password to log in. For example, in the image displayed above the token is `b66e74a85bc2570bf15782e5124c933c3a4ddabd2cf2d7d3`.

2. Select a notebook sample from the Overview notebook found in directory where you launched the server. In this example, the `intel/deep-learning:pytorch-latest-py3.11` container has a notebook titled [`Deep_Learning_Samples_Overview.ipynb`](https://github.com/intel/ai-containers/blob/main/preset/deep-learning-pytorch/notebooks/Deep_Learning_Samples_Overview.ipynb) when launched in Jupyter mode.

3. After selecting a notebook sample, choose the appropriate kernel from the dropdown menu available when loading the notebook. For each container, there is a kernel with the environment name: `jax-cpu`, `pytorch-cpu` and `pytorch-gpu`.

##### Advanced Jupyter Server Configuration

Modify your notebook server command by using the default example below to change the network (port/ip) and security (privilege) settings by appending it to the Docker run commands above:

```bash
docker run ... intel/deep-learning:pytorch-latest-py3.11 \
    bash -c "jupyter notebook --notebook-dir=~/jupyter \
            --port 8888 \
            --ip 0.0.0.0 \
            --no-browser \
            --allow-root"
```

### Run in Interactive Mode

This mode provides an interactive shell for working directly with the container's bash environment. Use this command to start the container in an interactive mode:

#### Run on CPU

```bash
docker run -it --rm \
    -p 8888:8888 --shm-size=12G \
    -v ${PWD}:/home/dev/workdir \
    intel/deep-learning:pytorch-latest-py3.11 bash
```

#### Run on GPU

Identify your system's `RENDER` and `VIDEO` group values to enable [Intel® Data Center GPU Flex/Max Series](https://www.intel.com/content/www/us/en/products/details/discrete-gpus/data-center-gpu.html):

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
    intel/deep-learning:pytorch-gpu-latest-py3.11 bash
```

> [!NOTE]
> Some applications use shared memory to share data between processes. The default shared memory segment size for Docker containers is 64MB, which may be insufficient for multithreaded applications. Increase the shared memory size using `--shm-size`.

#### Next Steps

1. For each container, there is a kernel with the environment name: `jax`, `pytorch-cpu` and `pytorch-gpu`. Use the command below to activate the `pytorch-cpu` environment in the Deep Learning PyTorch\* CPU preset:

    ```bash
    conda activate pytorch-cpu
    ```

2. Select a test from the `sample-tests` folder and run it using the following command as an example:

    ```bash
    python sample-tests/intel_extension_for_pytorch/test_ipex.py
    ```

    The `test_ipex.py` script utilizes PyTorch\* to classify images with a pre-trained ResNet-50 model.
    Users can specify whether to run the script on a CPU or XPU, and there is an option to apply optimizations using Intel® Extension for PyTorch\*.
    The script transfers both the model and data to the chosen device, and then measures the average inference time over 100 runs, excluding the initial warm-up phase.
    Finally, the script prints the average inference time.

> [!NOTE]
> The `sample-tests` folder may vary by container. Some tests use a bash script.

## Run in Multi-Node Distributed Mode [Advanced]

Follow the instructions provided for [Intel® Extension for PyTorch\*](https://github.com/intel/ai-containers/tree/main/preset/deep-learning/demo/pytorch-distributed/README.md) using the Deep Learning PyTorch\* GPU presets, respectively.

## Troubleshooting and Support

If you face any issues while using the container, refer to the [troubleshooting section](https://github.com/intel/ai-containers#troubleshooting). For additional assistance, you can submit an [issue](https://github.com/intel/ai-containers/issues).

---

\*Other names and brands may be claimed as the property of others. [Trademarks](http://www.intel.com/content/www/us/en/legal/trademarks.html)
