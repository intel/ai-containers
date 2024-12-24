# Intel® Extension for Pytorch\*

[Intel® Extension for PyTorch*] extends [PyTorch*] with up-to-date feature optimizations for an extra performance boost on Intel hardware.

On Intel CPUs optimizations take advantage of the following instuction sets:

* Intel® Advanced Matrix Extensions (Intel® AMX)
* Intel® Advanced Vector Extensions 512 (Intel® AVX-512)
* Vector Neural Network Instructions (VNNI)

On Intel GPUs Intel® Extension for PyTorch\* provides easy GPU acceleration through the PyTorch* `xpu` device. The following Intel GPUs are supported:

* [Intel® Arc™ A-Series Graphics]
* [Intel® Data Center GPU Flex Series]
* [Intel® Data Center GPU Max Series]

Images available here start with the [Ubuntu* 22.04](https://hub.docker.com/_/ubuntu) base image with [Intel® Extension for PyTorch*] built for different use cases as well as some additional software. The [Python Dockerfile](https://github.com/intel/ai-containers/blob/main/python/Dockerfile) is used to generate The images below at https://github.com/intel/ai-containers.

> **Note:** There are two dockerhub repositories (`intel/intel-extension-for-pytorch` and `intel/intel-optimized-pytorch`) that are routinely updated with the latest images, however, some legacy images have not be published to both repositories.

## XPU images

The images below include support for both CPU and GPU optimizations:

| Tag(s)                 | Pytorch  | IPEX           | Driver | Dockerfile      |
| ---------------------- | -------- | -------------- | ------ | --------------- |
| `2.5.10-xpu-pip-base`,`2.5.10-xpu` | [v2.5.1] | [v2.5.10+xpu] | [1057] | [v0.4.0-Beta]  |
| `2.3.110-xpu-pip-base`,`2.3.110-xpu` | [v2.3.1][torch-v2.3.1] | [v2.3.110+xpu] | [950]  | [v0.4.0-Beta]  |
| `2.1.40-xpu-pip-base`,`2.1.40-xpu`   | [v2.1.0] | [v2.1.40+xpu]  | [914]  | [v0.4.0-Beta]   |
| `2.1.30-xpu`           | [v2.1.0] | [v2.1.30+xpu]  | [803]  | [v0.4.0-Beta]   |
| `2.1.20-xpu`           | [v2.1.0] | [v2.1.20+xpu]  | [803]  | [v0.3.4]        |
| `2.1.10-xpu`           | [v2.1.0] | [v2.1.10+xpu]  | [736]  | [v0.2.3]        |
| `xpu-flex-2.0.110-xpu` | [v2.0.1] | [v2.0.110+xpu] | [647]  | [v0.1.0]        |

---

```bash
docker run -it --rm \
    --device /dev/dri \
    -v /dev/dri/by-path:/dev/dri/by-path \
    --ipc=host \
    intel/intel-extension-for-pytorch:2.5.10-xpu
```

---

The images below additionally include [Jupyter Notebook](https://jupyter.org/) server:

| Tag(s)                | Pytorch  | IPEX          | Driver | Jupyter Port | Dockerfile      |
| --------------------- | -------- | ------------- | ------ | ------------ | --------------- |
| `2.5.10-xpu-pip-jupyter` | [v2.5.1]| [v2.5.10+xpu] | [1057]  |  `8888` | [v0.4.0-Beta]  |
| `2.3.110-xpu-pip-jupyter` | [v2.3.1][torch-v2.3.1] | [v2.3.110+xpu] | [950]  | `8888`     | [v0.4.0-Beta]   |
| `2.1.40-xpu-pip-jupyter` | [v2.1.0] | [v2.1.40+xpu] | [914]  | `8888`     | [v0.4.0-Beta]   |
| `2.1.20-xpu-pip-jupyter` | [v2.1.0] | [v2.1.20+xpu] | [803]  | `8888`    | [v0.3.4]        |
| `2.1.10-xpu-pip-jupyter` | [v2.1.0] | [v2.1.10+xpu] | [736]  | `8888`    | [v0.2.3]        |

### Run the XPU Jupyter Container

```bash
docker run -it --rm \
    -p 8888:8888 \
    --device /dev/dri \
    -v /dev/dri/by-path:/dev/dri/by-path \
    intel/intel-extension-for-pytorch:2.5.10-xpu-pip-jupyter
```

After running the command above, copy the URL (something like `http://127.0.0.1:$PORT/?token=***`) into your browser to access the notebook server.

## CPU only images

The images below are built only with CPU optimizations (GPU acceleration support was deliberately excluded):

| Tag(s)                     | Pytorch  | IPEX         | Dockerfile      |
| -------------------------- | -------- | ------------ | --------------- |
| `2.5.0-pip-base`, `latest` | [v2.5.0] | [v2.5.0+cpu] | [v0.4.0-Beta]   |
| `2.4.0-pip-base`           | [v2.4.0] | [v2.4.0+cpu] | [v0.4.0-Beta]   |
| `2.3.0-pip-base`           | [v2.3.0] | [v2.3.0+cpu] | [v0.4.0-Beta]   |
| `2.2.0-pip-base`           | [v2.2.0] | [v2.2.0+cpu] | [v0.3.4]        |
| `2.1.0-pip-base`           | [v2.1.0] | [v2.1.0+cpu] | [v0.2.3]        |
| `2.0.0-pip-base`           | [v2.0.0] | [v2.0.0+cpu] | [v0.1.0]        |

### Run the CPU Container

```bash
docker run -it --rm intel/intel-extension-for-pytorch:latest
```

---

The images below additionally include [Jupyter Notebook](https://jupyter.org/) server:

| Tag(s)              | Pytorch  | IPEX         | Dockerfile      |
| ------------------- | -------- | ------------ | --------------- |
| `2.5.0-pip-jupyter` | [v2.5.0] | [v2.5.0+cpu] | [v0.4.0-Beta]   |
| `2.4.0-pip-jupyter` | [v2.4.0] | [v2.4.0+cpu] | [v0.4.0-Beta]   |
| `2.3.0-pip-jupyter` | [v2.3.0] | [v2.3.0+cpu] | [v0.4.0-Beta]   |
| `2.2.0-pip-jupyter` | [v2.2.0] | [v2.2.0+cpu] | [v0.3.4]        |
| `2.1.0-pip-jupyter` | [v2.1.0] | [v2.1.0+cpu] | [v0.2.3]        |
| `2.0.0-pip-jupyter` | [v2.0.0] | [v2.0.0+cpu] | [v0.1.0]        |

```bash
docker run -it --rm \
    -p 8888:8888 \
    -v $PWD/workspace:/workspace \
    -w /workspace \
    intel/intel-extension-for-pytorch:2.4.0-pip-jupyter
```

After running the command above, copy the URL (something like `http://127.0.0.1:$PORT/?token=***`) into your browser to access the notebook server.

---

The images below additionally include [Intel® oneAPI Collective Communications Library] (oneCCL) and Neural Compressor ([INC]):

| Tag(s)                  | Pytorch  | IPEX           | oneCCL               | INC       | Dockerfile     |
| ---------------------   | -------- | ------------   | -------------------- | --------- | -------------- |
| `2.4.0-pip-multinode`   | [v2.4.0] | [v2.4.0+cpu]   | [v2.4.0][ccl-v2.4.0] | [v3.0]    | [v0.4.0-Beta]  |
| `2.3.0-pip-multinode`   | [v2.3.0] | [v2.3.0+cpu]   | [v2.3.0][ccl-v2.3.0] | [v2.6]    | [v0.4.0-Beta]  |
| `2.2.0-pip-multinode`   | [v2.2.2] | [v2.2.0+cpu]   | [v2.2.0][ccl-v2.2.0] | [v2.6]    | [v0.4.0-Beta]  |
| `2.1.100-pip-mulitnode` | [v2.1.2] | [v2.1.100+cpu] | [v2.1.0][ccl-v2.1.0] | [v2.6]    | [v0.4.0-Beta]  |
| `2.0.100-pip-multinode` | [v2.0.1] | [v2.0.100+cpu] | [v2.0.0][ccl-v2.0.0] | [v2.6]    | [v0.4.0-Beta]  |

> [!NOTE]
> Passwordless SSH connection is also enabled in the image, but the container does not contain any SSH ID keys. The user needs to mount those keys at `/root/.ssh/id_rsa` and `/etc/ssh/authorized_keys`.

> [!TIP]
> Before mounting any keys, modify the permissions of those files with `chmod 600 authorized_keys; chmod 600 id_rsa` to grant read access for the default user account.

#### Setup and Run IPEX Multi-Node Container

> [!IMPORTANT]
> Maintainence, Bug Fixes, and Releases of [Intel® Extension for PyTorch*] Multi-Node Container for Xeon Processors have ceased development. The last supported version is `2.4.0`. For future releases, please use the [Intel® Extension for PyTorch*] Multi-Node Container for XPU.

Some additional assembly is required to utilize this container with OpenSSH. To perform any kind of DDP (Distributed Data Parallel) execution, containers are assigned the roles of launcher and worker respectively:

SSH Server (Worker)

1. *Authorized Keys* : `/etc/ssh/authorized_keys`

SSH Client (Launcher)

1. *Private User Key* : `/root/.ssh/id_rsa`

To add these files correctly please follow the steps described below.

1. Setup ID Keys

    You can use the commands provided below to [generate the identity keys](https://www.ssh.com/academy/ssh/keygen#creating-an-ssh-key-pair-for-user-authentication) for OpenSSH.

    ```bash
    ssh-keygen -q -N "" -t rsa -b 4096 -f ./id_rsa
    touch authorized_keys
    cat id_rsa.pub >> authorized_keys
    ```

2. Configure the permissions and ownership for all of the files you have created so far

    ```bash
    chmod 600 id_rsa config authorized_keys
    chown root:root id_rsa.pub id_rsa config authorized_keys
    ```

3. Create a hostfile for `torchrun` or `ipexrun`. (Optional)

    ```txt
    Host host1
        HostName <Hostname of host1>
        IdentitiesOnly yes
        IdentityFile ~/.root/id_rsa
        Port <SSH Port>
    Host host2
        HostName <Hostname of host2>
        IdentitiesOnly yes
        IdentityFile ~/.root/id_rsa
        Port <SSH Port>
    ...
    ```

4. Configure [Intel® oneAPI Collective Communications Library] in your python script

    ```python
    import oneccl_bindings_for_pytorch
    import os

    dist.init_process_group(
        backend="ccl",
        init_method="tcp://127.0.0.1:3022",
        world_size=int(os.environ.get("WORLD_SIZE")),
        rank=int(os.environ.get("RANK")),
    )
    ```

5. Now start the workers and execute DDP on the launcher

    1. Worker run command:

        ```bash
        docker run -it --rm \
            --net=host \
            -v $PWD/authorized_keys:/etc/ssh/authorized_keys \
            -v $PWD/tests:/workspace/tests \
            -w /workspace \
            intel/intel-extension-for-pytorch:2.4.0-pip-multinode \
            bash -c '/usr/sbin/sshd -D'
        ```

    2. Launcher run command:

        ```bash
        docker run -it --rm \
            --net=host \
            -v $PWD/id_rsa:/root/.ssh/id_rsa \
            -v $PWD/tests:/workspace/tests \
            -v $PWD/hostfile:/workspace/hostfile \
            -w /workspace \
            intel/intel-extension-for-pytorch:2.4.0-pip-multinode \
            bash -c 'ipexrun cpu  --nnodes 2 --nprocs-per-node 1 --master-addr 127.0.0.1 --master-port 3022 /workspace/tests/ipex-resnet50.py --ipex --device cpu --backend ccl'
        ```

> [!NOTE]
> [Intel® MPI] can be configured based on your machine settings. If the above commands do not work for you, see the documentation for how to configure based on your network.

#### Enable [DeepSpeed*] optimizations

To enable [DeepSpeed*] optimizations with [Intel® oneAPI Collective Communications Library], add the following to your python script:

```python
import deepspeed

# Rather than dist.init_process_group(), use deepspeed.init_distributed()
deepspeed.init_distributed(backend="ccl")
```

Additionally, if you have a [DeepSpeed* configuration](https://www.deepspeed.ai/getting-started/#deepspeed-configuration) you can use the below command as your launcher to run your script with that configuration:

```bash
    docker run -it --rm \
    --net=host \
    -v $PWD/id_rsa:/root/.ssh/id_rsa \
    -v $PWD/tests:/workspace/tests \
    -v $PWD/hostfile:/workspace/hostfile \
    -v $PWD/ds_config.json:/workspace/ds_config.json \
    -w /workspace \
    intel/intel-extension-for-pytorch:2.4.0-pip-multinode \
    bash -c 'deepspeed --launcher IMPI \
    --master_addr 127.0.0.1 --master_port 3022 \
    --deepspeed_config ds_config.json --hostfile /workspace/hostfile \
    /workspace/tests/ipex-resnet50.py --ipex --device cpu --backend ccl --deepspeed'
```

---

The image below is an extension of the IPEX Multi-Node Container designed to run Hugging Face Generative AI scripts. The container has the typical installations needed to run and fine tune PyTorch generative text models from Hugging Face. It can be used to run multinode jobs using the same instructions from the [IPEX Multi-Node container](#setup-and-run-ipex-multi-node-container).

| Tag(s)                                | Pytorch  | IPEX         | oneCCL               | HF Transformers | Dockerfile      |
| ------------------------------------- | -------- | ------------ | -------------------- | --------------- | --------------- |
| `2.4.0-pip-multinode-hf-4.44.0-genai` | [v2.4.0] | [v2.4.0+cpu] | [v2.4.0][ccl-v2.4.0] | [v4.44.0]       | [v0.4.0-Beta]   |

Below is an example that shows single node job with the existing [`finetune.py`](../workflows/charts/huggingface-llm/scripts/finetune.py) script.

```bash
# Change into home directory first and run the command
docker run -it \
    -v $PWD/workflows/charts/huggingface-llm/scripts:/workspace/scripts \
    -w /workspace/scripts \
    intel/intel-extension-for-pytorch:2.4.0-pip-multinode-hf-4.44.0-genai \
    bash -c 'python finetune.py <script-args>'
```

---

The images below are [TorchServe*] with CPU Optimizations:

| Tag(s)              | Pytorch  | IPEX         | Dockerfile      |
| ------------------- | -------- | ------------ | --------------- |
| `2.5.0-serving-cpu` | [v2.5.0] | [v2.5.0+cpu] | [v0.4.0-Beta]   |
| `2.4.0-serving-cpu` | [v2.4.0] | [v2.4.0+cpu] | [v0.4.0-Beta]   |
| `2.3.0-serving-cpu` | [v2.3.0] | [v2.3.0+cpu] | [v0.4.0-Beta]   |
| `2.2.0-serving-cpu` | [v2.2.0] | [v2.2.0+cpu] | [v0.3.4]        |

For more details, follow the procedure in the [TorchServe](https://github.com/pytorch/serve/blob/master/examples/intel_extension_for_pytorch/README.md) instructions.

The images below are [TorchServe*] with XPU Optimizations:

| Tag(s)              | Pytorch  | IPEX         | Dockerfile      |
| ------------------- | -------- | ------------ | --------------- |
| `2.3.110-serving-xpu` | [v2.3.1][torch-v2.3.1] | [v2.3.110+xpu] | [v0.4.0-Beta]   |

## CPU only images with Intel® Distribution for Python*

The images below are built only with CPU optimizations (GPU acceleration support was deliberately excluded) and include [Intel® Distribution for Python*]:

| Tag(s)           | Pytorch  | IPEX         | Dockerfile      |
| ---------------- | -------- | ------------ | --------------- |
| `2.5.0-idp-base` | [v2.5.0] | [v2.5.0+cpu] | [v0.4.0-Beta]   |
| `2.4.0-idp-base` | [v2.4.0] | [v2.4.0+cpu] | [v0.4.0-Beta]   |
| `2.3.0-idp-base` | [v2.3.0] | [v2.3.0+cpu] | [v0.4.0-Beta]   |
| `2.2.0-idp-base` | [v2.2.0] | [v2.2.0+cpu] | [v0.3.4]        |
| `2.1.0-idp-base` | [v2.1.0] | [v2.1.0+cpu] | [v0.2.3]        |
| `2.0.0-idp-base` | [v2.0.0] | [v2.0.0+cpu] | [v0.1.0]        |

The images below additionally include [Jupyter Notebook](https://jupyter.org/) server:

| Tag(s)              | Pytorch  | IPEX         | Dockerfile      |
| ------------------- | -------- | ------------ | --------------- |
| `2.5.0-idp-jupyter` | [v2.5.0] | [v2.5.0+cpu] | [v0.4.0-Beta]   |
| `2.4.0-idp-jupyter` | [v2.4.0] | [v2.4.0+cpu] | [v0.4.0-Beta]   |
| `2.3.0-idp-jupyter` | [v2.3.0] | [v2.3.0+cpu] | [v0.4.0-Beta]   |
| `2.2.0-idp-jupyter` | [v2.2.0] | [v2.2.0+cpu] | [v0.3.4]        |
| `2.1.0-idp-jupyter` | [v2.1.0] | [v2.1.0+cpu] | [v0.2.3]        |
| `2.0.0-idp-jupyter` | [v2.0.0] | [v2.0.0+cpu] | [v0.1.0]        |

The images below additionally include [Intel® oneAPI Collective Communications Library] (oneCCL) and Neural Compressor ([INC]):

| Tag(s)                | Pytorch  | IPEX         | oneCCL               | INC       | Dockerfile      |
| --------------------- | -------- | ------------ | -------------------- | --------- | --------------- |
| `2.4.0-idp-multinode` | [v2.4.0] | [v2.4.0+cpu] | [v2.4.0][ccl-v2.3.0] | [v3.0]    | [v0.4.0-Beta]   |
| `2.3.0-idp-multinode` | [v2.3.0] | [v2.3.0+cpu] | [v2.3.0][ccl-v2.3.0] | [v2.6]    | [v0.4.0-Beta]   |
| `2.2.0-idp-multinode` | [v2.2.0] | [v2.2.0+cpu] | [v2.2.0][ccl-v2.2.0] | [v2.4.1]  | [v0.3.4]        |
| `2.1.0-idp-mulitnode` | [v2.1.0] | [v2.1.0+cpu] | [v2.1.0][ccl-v2.1.0] | [v2.3.1]  | [v0.2.3]        |
| `2.0.0-idp-multinode` | [v2.0.0] | [v2.0.0+cpu] | [v2.0.0][ccl-v2.0.0] | [v2.1.1]  | [v0.1.0]        |

## XPU images with Intel® Distribution for Python*

The images below are built only with CPU and GPU optimizations and include [Intel® Distribution for Python*]:

| Tag(s)           | Pytorch  | IPEX         | Driver | Dockerfile      |
| ---------------- | -------- | ------------ | -------- | ------ |
| `2.5.10-xpu-idp-base`| [v2.5.1] | [v2.5.10+xpu] | [1057]  | [v0.4.0-Beta]  |
| `2.3.110-xpu-idp-base` | [v2.3.1][torch-v2.3.1] | [v2.3.110+xpu] | [950]  | [v0.4.0-Beta] |
| `2.1.40-xpu-idp-base` | [v2.1.0] | [v2.1.40+xpu] | [914]  | [v0.4.0-Beta] |
| `2.1.30-xpu-idp-base` | [v2.1.0] | [v2.1.30+xpu]  | [803]  | [v0.4.0-Beta] |
| `2.1.10-xpu-idp-base` | [v2.1.0] | [v2.1.10+xpu]  | [736]  | [v0.2.3] |

The images below additionally include [Jupyter Notebook](https://jupyter.org/) server:

| Tag(s)                | Pytorch  | IPEX          | Driver | Jupyter Port | Dockerfile      |
| --------------------- | -------- | ------------- | ------ | ------------ | --------------- |
| `2.5.10-xpu-idp-jupyter` | [v2.5.1] | [v2.5.10+xpu] | [1057]  |  `8888` | [v0.4.0-Beta]  |
| `2.3.110-xpu-idp-jupyter` | [v2.3.1][torch-v2.3.1] | [v2.3.110+xpu] | [950]  | `8888` | [v0.4.0-Beta] |
| `2.1.40-xpu-idp-jupyter` | [v2.1.0] | [v2.1.40+xpu] | [914]  | `8888`   | [v0.4.0-Beta]   |
| `2.1.20-xpu-idp-jupyter` | [v2.1.0] | [v2.1.20+xpu] | [803]  | `8888`   | [v0.3.4]        |
| `2.1.10-xpu-idp-jupyter` | [v2.1.0] | [v2.1.10+xpu] | [736]  | `8888`   | [v0.2.3]        |

## Build from Source

To build the images from source, clone the [AI Containers](https://github.com/intel/ai-containers) repository, follow the main `README.md` file to setup your environment, and run the following command:

```bash
cd pytorch
docker compose build ipex-base
docker compose run ipex-base
```

You can find the list of services below for each container in the group:

| Service Name  | Description                                                         |
| ------------- | ------------------------------------------------------------------- |
| `ipex-base`   | Base image with [Intel® Extension for PyTorch*]                     |
| `jupyter`     | Adds Jupyter Notebook server                                        |
| `multinode`   | Adds [Intel® oneAPI Collective Communications Library] and [INC]    |
| `xpu`         | Adds Intel GPU Support                                              |
| `xpu-jupyter` | Adds Jupyter notebook server to GPU image                           |
| `serving`     | [TorchServe*]                                                       |

## MLPerf Optimized Workloads

The following images are available for MLPerf-optimized workloads. Instructions are available at '[Get Started with Intel MLPerf]'.

| Tag(s)                            | Base OS        | MLPerf Round     | Target Platform                 |
| --------------------------------- | -------------- | ---------------- | ------------------------------- |
| `mlperf-inference-4.1-resnet50`   | rockylinux:8.7 | [Inference v4.1] | Intel(R) Xeon(R) Platinum 8592+ |
| `mlperf-inference-4.1-retinanet`  | ubuntu:22.04   | [Inference v4.1] | Intel(R) Xeon(R) Platinum 8592+ |
| `mlperf-inference-4.1-gptj`       | ubuntu:22.04   | [Inference v4.1] | Intel(R) Xeon(R) Platinum 8592+ |
| `mlperf-inference-4.1-bert`       | ubuntu:22.04   | [Inference v4.1] | Intel(R) Xeon(R) Platinum 8592+ |
| `mlperf-inference-4.1-dlrmv2`     | rockylinux:8.7 | [Inference v4.1] | Intel(R) Xeon(R) Platinum 8592+ |
| `mlperf-inference-4.1-3dunet`     | ubuntu:22.04   | [Inference v4.1] | Intel(R) Xeon(R) Platinum 8592+ |

## License

View the [License](https://github.com/intel/intel-extension-for-pytorch/blob/main/LICENSE) for the [Intel® Extension for PyTorch*].

The images below also contain other software which may be under other licenses (such as Pytorch*, Jupyter*, Bash, etc. from the base).

It is the image user's responsibility to ensure that any use of The images below comply with any relevant licenses for all software contained within.

\* Other names and brands may be claimed as the property of others.

<!--Below are links used in these document. They are not rendered: -->

[Intel® Arc™ A-Series Graphics]: https://ark.intel.com/content/www/us/en/ark/products/series/227957/intel-arc-a-series-graphics.html
[Intel® Data Center GPU Flex Series]: https://ark.intel.com/content/www/us/en/ark/products/series/230021/intel-data-center-gpu-flex-series.html
[Intel® Data Center GPU Max Series]: https://ark.intel.com/content/www/us/en/ark/products/series/232874/intel-data-center-gpu-max-series.html

[Intel® MPI]: https://www.intel.com/content/www/us/en/developer/tools/oneapi/mpi-library.html
[Intel® Extension for PyTorch*]: https://intel.github.io/intel-extension-for-pytorch/
[Intel® Distribution for Python*]: https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-for-python.html
[Intel® oneAPI Collective Communications Library]: https://www.intel.com/content/www/us/en/developer/tools/oneapi/oneccl.html
[INC]: https://github.com/intel/neural-compressor
[PyTorch*]: https://pytorch.org/
[TorchServe*]: https://github.com/pytorch/serve
[DeepSpeed*]: https://github.com/microsoft/DeepSpeed

[v0.4.0-Beta]: https://github.com/intel/ai-containers/blob/main/pytorch/Dockerfile
[v0.3.4]: https://github.com/intel/ai-containers/blob/v0.3.4/pytorch/Dockerfile
[v0.2.3]: https://github.com/intel/ai-containers/blob/v0.2.3/pytorch/Dockerfile
[v0.1.0]: https://github.com/intel/ai-containers/blob/v0.1.0/pytorch/Dockerfile

[v2.5.10+xpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.5.10%2Bxpu
[v2.3.110+xpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.3.110%2Bxpu
[v2.1.40+xpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.1.40%2Bxpu
[v2.1.30+xpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.1.30%2Bxpu
[v2.1.20+xpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.1.20%2Bxpu
[v2.1.10+xpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.1.10%2Bxpu
[v2.0.110+xpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.0.110%2Bxpu

[v2.5.1]: https://github.com/pytorch/pytorch/releases/tag/v2.5.1
[v2.5.0]: https://github.com/pytorch/pytorch/releases/tag/v2.5.0
[v2.4.0]: https://github.com/pytorch/pytorch/releases/tag/v2.4.0
[v2.3.0]: https://github.com/pytorch/pytorch/releases/tag/v2.3.0
[v2.2.2]: https://github.com/pytorch/pytorch/releases/tag/v2.2.2
[v2.2.0]: https://github.com/pytorch/pytorch/releases/tag/v2.2.0
[v2.1.2]: https://github.com/pytorch/pytorch/releases/tag/v2.1.2
[v2.1.0]: https://github.com/pytorch/pytorch/releases/tag/v2.1.0
[v2.0.1]: https://github.com/pytorch/pytorch/releases/tag/v2.0.1
[v2.0.0]: https://github.com/pytorch/pytorch/releases/tag/v2.0.0

[torch-v2.3.1]: https://github.com/pytorch/pytorch/tree/v2.3.1

[v3.0]: https://github.com/intel/neural-compressor/releases/tag/v3.0
[v2.6]: https://github.com/intel/neural-compressor/releases/tag/v2.6
[v2.4.1]: https://github.com/intel/neural-compressor/releases/tag/v2.4.1
[v2.3.1]: https://github.com/intel/neural-compressor/releases/tag/v2.3.1
[v2.1.1]: https://github.com/intel/neural-compressor/releases/tag/v2.1.1

[v2.5.0+cpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.5.0%2Bcpu
[v2.4.0+cpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.4.0%2Bcpu
[v2.3.0+cpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.3.0%2Bcpu
[v2.2.0+cpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.2.0%2Bcpu
[v2.1.100+cpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.1.0%2Bcpu
[v2.1.0+cpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.1.0%2Bcpu
[v2.0.100+cpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.0.0%2Bcpu
[v2.0.0+cpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.0.0%2Bcpu

[ccl-v2.4.0]: https://github.com/intel/torch-ccl/releases/tag/v2.4.0%2Bcpu%2Brc0
[ccl-v2.3.0]: https://github.com/intel/torch-ccl/releases/tag/v2.3.0%2Bcpu
[ccl-v2.2.0]: https://github.com/intel/torch-ccl/releases/tag/v2.2.0%2Bcpu
[ccl-v2.1.0]: https://github.com/intel/torch-ccl/releases/tag/v2.1.0%2Bcpu
[ccl-v2.0.0]: https://github.com/intel/torch-ccl/releases/tag/v2.1.0%2Bcpu

<!-- HuggingFace transformers releases -->
[v4.44.0]: https://github.com/huggingface/transformers/releases/tag/v4.44.0

[1057]: https://dgpu-docs.intel.com/releases/packages.html?release=Rolling+2448.13&os=Ubuntu+22.04
[950]: https://dgpu-docs.intel.com/releases/stable_950_13_20240814.html
[914]: https://dgpu-docs.intel.com/releases/stable_914_33_20240730.html
[803]: https://dgpu-docs.intel.com/releases/LTS_803.29_20240131.html
[736]: https://dgpu-docs.intel.com/releases/stable_736_25_20231031.html
[647]: https://dgpu-docs.intel.com/releases/stable_647_21_20230714.html

<!-- MLPerf Dashboard -->
[Inference v4.1]: https://mlcommons.org/benchmarks/inference-datacenter
[Get Started with Intel MLPerf]: https://www.intel.com/content/www/us/en/developer/articles/guide/get-started-mlperf-intel-optimized-docker-images.html
