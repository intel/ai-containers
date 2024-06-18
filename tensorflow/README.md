# Intel® Extension for TensorFlow\*

[Intel® Extension for TensorFlow*] extends [TensorFlow*] with up-to-date feature optimizations for an extra performance boost on Intel hardware.

[Intel® Extension for TensorFlow*] is based on the TensorFlow [PluggableDevice] interface to bring Intel XPU(GPU, CPU, etc.) devices into [TensorFlow*] with flexibility for on-demand performance on the following Intel GPUs:

* [Intel® Arc™ A-Series Graphics]
* [Intel® Data Center GPU Flex Series]
* [Intel® Data Center GPU Max Series]

> **Note:** There are two dockerhub repositories (`intel/intel-extension-for-tensorflow` and `intel/intel-optimized-tensorflow`) that are routinely updated with the latest images, however, some legacy images have not be published to both repositories.

## XPU images

The images below include support for both CPU and GPU optimizations:

| Tag(s)                 | TensorFlow  | ITEX           | Driver | Dockerfile      |
| ---------------------- | ----------- | -------------- | ------ | --------------- |
| `2.15.0.0-xpu`, `xpu`  | [v2.15.0]   | [v2.15.0.0]    | [803]  | [v0.4.0-Beta]   |
| `2.14.0.1-xpu`         | [v2.14.1]   | [v2.14.0.1]    | [736]  | [v0.3.4]        |
| `2.13.0.0-xpu`         | [v2.13.0]   | [v2.13.0.0]    | [647]  | [v0.2.3]        |

### Run the XPU Container

```bash
docker run -it --rm \
    --device /dev/dri \
    -v /dev/dri/by-path:/dev/dri/by-path \
    --ipc=host \
    intel/intel-extension-for-tensorflow:xpu
```

---

The images below additionally include [Jupyter Notebook](https://jupyter.org/) server:

| Tag(s)        | TensorFlow  | IPEX          | Driver | Dockerfile      |
| ------------- | ----------- | ------------- | ------ | --------------- |
| `xpu-jupyter` | [v2.14.1]   | [v2.14.0.1]   | [736]  | [v0.3.4]   |

### Run the XPU Jupyter Container

```bash
docker run -it --rm \
    -p 8888:8888 \
    --net=host \
    --device /dev/dri \
    -v /dev/dri/by-path:/dev/dri/by-path \
    --ipc=host \
    intel/intel-extension-for-tensorflow:xpu-jupyter
```

After running the command above, copy the URL (something like `http://127.0.0.1:$PORT/?token=***`) into your browser to access the notebook server.

---

The images below are [TensorFlow* Serving] with GPU Optimizations:

| Tag(s)                                | TensorFlow  | IPEX         |
| ------------------------------------- | ----------- | ------------ |
| `2.14.0.1-serving-gpu`, `serving-gpu` | [v2.14.1]   | [v2.14.0.1]  |
| `2.13.0.0-serving-gpu`,               | [v2.13.0]   | [v2.13.0.0]  |

### Run the Serving GPU Container

```bash
docker run -it --rm \
    -p 8500:8500 \
    --device /dev/dri \
    -v /dev/dri/by-path:/dev/dri/by-path \
    -v $PWD/workspace:/workspace \
    -w /workspace \
    -e MODEL_NAME=<your-model-name> \
    -e MODEL_DIR=<your-model-dir> \
    intel/intel-extension-for-tensorflow:serving-gpu
```

For more details, follow the procedure in the [Intel® Extension for TensorFlow* Serving] instructions.

## CPU only images

The images below are built only with CPU optimizations (GPU acceleration support was deliberately excluded):

| Tag(s)                      | TensorFlow  | ITEX         | Dockerfile      |
| --------------------------- | ----------- | ------------ | --------------- |
| `2.15.0-pip-base`, `latest` | [v2.15.0]   | [v2.15.0.0]  | [v0.4.0-Beta]   |
| `2.14.0-pip-base`           | [v2.14.1]   | [v2.14.0.1]  | [v0.3.4]        |
| `2.13-pip-base`             | [v2.13.0]   | [v2.13.0.0]  | [v0.2.3]        |

The images below additionally include [Jupyter Notebook](https://jupyter.org/) server:

| Tag(s)               | TensorFlow  | ITEX          | Dockerfile      |
| -------------------- | ----------- | ------------- | --------------- |
| `2.15.0-pip-jupyter` | [v2.15.0]   | [v2.15.0.0]   | [v0.4.0-Beta]   |
| `2.14.0-pip-jupyter` | [v2.14.1]   | [v2.14.0.1]   | [v0.3.4]        |
| `2.13-pip-jupyter`   | [v2.13.0]   | [v2.13.0.0]   | [v0.2.3]        |

### Run the CPU Jupyter Container

```bash
docker run -it --rm \
    -p 8888:8888 \
    --net=host \
    -v $PWD/workspace:/workspace \
    -w /workspace \
    intel/intel-extension-for-tensorflow:xpu-jupyter
```

After running the command above, copy the URL (something like `http://127.0.0.1:$PORT/?token=***`) into your browser to access the notebook server.

---

The images below additionally include [Horovod]:

| Tag(s)                         | Tensorflow  | ITEX         | Horovod   | Dockerfile      |
| ------------------------------ | ---------   | ------------ | --------- | --------------- |
| `2.15.0-pip-multinode`         | [v2.15.0]   | [v2.15.0.0]  | [v0.28.1] | [v0.4.0-Beta]   |
| `2.14.0-pip-openmpi-multinode` | [v2.14.1]   | [v2.14.0.1]  | [v0.28.1] | [v0.3.4]        |
| `2.13-pip-openmpi-mulitnode`   | [v2.13.0]   | [v2.13.0.0]  | [v0.28.0] | [v0.2.3]        |

---

The images below are [TensorFlow* Serving] with CPU Optimizations:

| Tag(s)                                | TensorFlow | ITEX         |
| ------------------------------------- | ---------- | ------------ |
| `2.14.0.1-serving-cpu`, `serving-cpu` | [v2.14.1]  | [v2.14.0.1]  |
| `2.13.0.0-serving-cpu`                | [v2.13.0]  | [v2.13.0.0]  |

### Run the Serving CPU Container

```bash
docker run -it --rm \
    -p 8500:8500 \
    --device /dev/dri \
    -v /dev/dri/by-path:/dev/dri/by-path \
    -v $PWD/workspace:/workspace \
    -w /workspace \
    -e MODEL_NAME=<your-model-name> \
    -e MODEL_DIR=<your-model-dir> \
    intel/intel-extension-for-tensorflow:serving-cpu
```

For more details, follow the procedure in the [Intel® Extension for TensorFlow* Serving] instructions.

## CPU only images with Intel® Distribution for Python*

The images below are built only with CPU optimizations (GPU acceleration support was deliberately excluded) and include [Intel® Distribution for Python*]:

| Tag(s)                      | TensorFlow  | ITEX         | Dockerfile      |
| --------------------------- | ----------- | ------------ | --------------- |
| `2.15.0-idp-base`, `latest` | [v2.15.0]   | [v2.15.0.0]  | [v0.4.0-Beta]   |
| `2.14.0-idp-base`           | [v2.14.1]   | [v2.14.0.1]  | [v0.3.4]        |
| `2.13-idp-base`             | [v2.13.0]   | [v2.13.0.0]  | [v0.2.3]        |

The images below additionally include [Jupyter Notebook](https://jupyter.org/) server:

| Tag(s)               | TensorFlow  | ITEX          | Dockerfile      |
| -------------------- | ----------- | ------------- | --------------- |
| `2.15.0-idp-jupyter` | [v2.15.0]   | [v2.15.0.0]   | [v0.4.0-Beta]   |
| `2.14.0-idp-jupyter` | [v2.14.1]   | [v2.14.0.1]   | [v0.3.4]        |
| `2.13-idp-jupyter`   | [v2.13.0]   | [v2.13.0.0]   | [v0.2.3]        |

The images below additionally include [Horovod]:

| Tag(s)                         | Tensorflow  | ITEX         | Horovod   | Dockerfile      |
| ------------------------------ | ---------   | ------------ | --------- | --------------- |
| `2.15.0-idp-multinode`         | [v2.15.0]   | [v2.15.0.0]  | [v0.28.1] | [v0.4.0-Beta]   |
| `2.14.0-idp-openmpi-multinode` | [v2.14.1]   | [v2.14.0.1]  | [v0.28.1] | [v0.3.4]        |
| `2.13-idp-openmpi-mulitnode`   | [v2.13.0]   | [v2.13.0.0]  | [v0.28.0] | [v0.2.3]        |

## Build from Source

To build the images from source, clone the [Intel® AI Containers](https://github.com/intel/ai-containers) repository, follow the main `README.md` file to setup your environment, and run the following command:

```bash
cd pytorch
docker compose build tf-base
docker compose run tf-base
```

You can find the list of services below for each container in the group:

| Service Name  | Description                                                         |
| ------------- | ------------------------------------------------------------------- |
| `tf-base`     | Base image with [Intel® Extension for TensorFlow*]                  |
| `jupyter`     | Adds Jupyter Notebook server                                        |
| `multinode`   | Adds [Intel® MPI], [Horovod] and [INC]                              |
| `xpu`         | Adds Intel GPU Support                                              |
| `xpu-jupyter` | Adds Jupyter notebook server to GPU image                           |

## License

View the [License](https://github.com/intel/intel-extension-for-tensorflow/tree/main?tab=License-1-ov-file#readme) for the [Intel® Extension for TensorFlow*].

The images below also contain other software which may be under other licenses (such as TensorFlow*, Jupyter*, Bash, etc. from the base).

It is the image user's responsibility to ensure that any use of The images below comply with any relevant licenses for all software contained within.

\* Other names and brands may be claimed as the property of others.

<!--Below are links used in these document. They are not rendered: -->

[Intel® Arc™ A-Series Graphics]: https://ark.intel.com/content/www/us/en/ark/products/series/227957/intel-arc-a-series-graphics.html
[Intel® Data Center GPU Flex Series]: https://ark.intel.com/content/www/us/en/ark/products/series/230021/intel-data-center-gpu-flex-series.html
[Intel® Data Center GPU Max Series]: https://ark.intel.com/content/www/us/en/ark/products/series/232874/intel-data-center-gpu-max-series.html

[Intel® Extension for TensorFlow*]: https://github.com/intel/intel-extension-for-tensorflow
[Intel® Extension for TensorFlow* Serving]: https://intel.github.io/intel-extension-for-tensorflow/latest/docker/tensorflow-serving/README.html
[Intel® Distribution for Python*]: https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-for-python.html
[INC]: https://github.com/intel/neural-compressor
[TensorFlow*]: https://github.com/tensorflow/tensorflow
[PluggableDevice]: https://github.com/tensorflow/community/blob/master/rfcs/20200624-pluggable-device-for-tensorflow.md
[TensorFlow* Serving]: https://github.com/tensorflow/serving
[Horovod]: https://github.com/horovod/horovod
[Intel® MPI]: https://www.intel.com/content/www/us/en/developer/tools/oneapi/mpi-library.html#gs.9bna9o

[v0.4.0-Beta]: https://github.com/intel/ai-containers/blob/v0.4.0-Beta/tensorflow/Dockerfile
[v0.3.4]: https://github.com/intel/ai-containers/blob/v0.3.4/tensorflow/Dockerfile
[v0.2.3]: https://github.com/intel/ai-containers/blob/v0.2.3/tensorflow/Dockerfile

[v2.15.0]: https://github.com/tensorflow/tensorflow/releases/tag/v2.15.0
[v2.14.1]: https://github.com/tensorflow/tensorflow/releases/tag/v2.14.1
[v2.13.0]: https://github.com/tensorflow/tensorflow/releases/tag/v2.13.0

[v2.15.0.0]: https://github.com/intel/intel-extension-for-tensorflow/releases/tag/v2.15.0.0
[v2.14.0.1]: https://github.com/intel/intel-extension-for-tensorflow/releases/tag/v2.14.0.1
[v2.13.0.0]: https://github.com/intel/intel-extension-for-tensorflow/releases/tag/v2.13.0.0

[v0.28.1]: https://github.com/horovod/horovod/releases/tag/v0.28.1
[v0.28.0]: https://github.com/horovod/horovod/releases/tag/v0.28.0

[803]: https://dgpu-docs.intel.com/releases/LTS_803.29_20240131.html
[736]: https://dgpu-docs.intel.com/releases/stable_736_25_20231031.html
[647]: https://dgpu-docs.intel.com/releases/stable_647_21_20230714.html
