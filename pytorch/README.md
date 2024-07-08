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
    intel/intel-extension-for-pytorch:2.1.30-xpu
```

---

The images below additionally include [Jupyter Notebook](https://jupyter.org/) server:

| Tag(s)                | Pytorch  | IPEX          | Driver | Jupyter Port | Dockerfile      |
| --------------------- | -------- | ------------- | ------ | ------------ | --------------- |
| `2.1.20-xpu-pip-jupyter` | [v2.1.0] | [v2.1.20+xpu] | [803]  | `8888`       | [v0.3.4]     |
| `2.1.20-xpu-idp-jupyter` | [v2.1.0] | [v2.1.20+xpu] | [803]  | `8888`       | [v0.3.4]     |
| `2.1.10-xpu-pip-jupyter` | [v2.1.0] | [v2.1.10+xpu] | [736]  | `8888`       | [v0.3.4]     |
| `2.1.10-xpu-idp-jupyter` | [v2.1.0] | [v2.1.10+xpu] | [736]  | `8888`       | [v0.3.4]     |

### Run the XPU Jupyter Container

```bash
docker run -it --rm \
    -p 8888:8888 \
    --net=host \
    --device /dev/dri \
    -v /dev/dri/by-path:/dev/dri/by-path \
    --ipc=host \
    intel/intel-extension-for-pytorch:2.1.20-xpu-pip-jupyter
```

After running the command above, copy the URL (something like `http://127.0.0.1:$PORT/?token=***`) into your browser to access the notebook server.

## CPU only images

The images below are built only with CPU optimizations (GPU acceleration support was deliberately excluded):

| Tag(s)                     | Pytorch  | IPEX         | Dockerfile      |
| -------------------------- | -------- | ------------ | --------------- |
| `2.3.0-pip-base`, `latest` | [v2.3.0] | [v2.3.0+cpu] | [v0.4.0-Beta]   |
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
| `2.3.0-pip-jupyter` | [v2.3.0] | [v2.3.0+cpu] | [v0.4.0-Beta]   |
| `2.2.0-pip-jupyter` | [v2.2.0] | [v2.2.0+cpu] | [v0.3.4]        |
| `2.1.0-pip-jupyter` | [v2.1.0] | [v2.1.0+cpu] | [v0.2.3]        |
| `2.0.0-pip-jupyter` | [v2.0.0] | [v2.0.0+cpu] | [v0.1.0]        |

```bash
docker run -it --rm \
    -p 8888:8888 \
    --net=host \
    -v $PWD/workspace:/workspace \
    -w /workspace \
    intel/intel-extension-for-pytorch:2.3.0-pip-jupyter
```

After running the command above, copy the URL (something like `http://127.0.0.1:$PORT/?token=***`) into your browser to access the notebook server.

---

The images below additionally include [Intel® oneAPI Collective Communications Library] (oneCCL) and Neural Compressor ([INC]):

| Tag(s)                | Pytorch  | IPEX         | oneCCL               | INC       | Dockerfile      |
| --------------------- | -------- | ------------ | -------------------- | --------- | --------------- |
| `2.3.0-pip-multinode` | [v2.3.0] | [v2.3.0+cpu] | [v2.3.0][ccl-v2.3.0] | [v2.5.1]  | [v0.4.0-Beta]   |
| `2.2.0-pip-multinode` | [v2.2.0] | [v2.2.0+cpu] | [v2.2.0][ccl-v2.2.0] | [v2.4.1]  | [v0.3.4]        |
| `2.1.0-pip-mulitnode` | [v2.1.0] | [v2.1.0+cpu] | [v2.1.0][ccl-v2.1.0] | [v2.3.1]  | [v0.2.3]        |
| `2.0.0-pip-multinode` | [v2.0.0] | [v2.0.0+cpu] | [v2.0.0][ccl-v2.0.0] | [v2.1.1]  | [v0.1.0]        |

> **Note:** Passwordless SSH connection is also enabled in the image.
> The container does not contain the SSH ID keys. The user needs to mount those keys at `/root/.ssh/id_rsa` and `/root/.ssh/id_rsa.pub`.
> User also need to append content of id_rsa.pub in `/etc/ssh/authorized_keys` in the SSH server container.
> Since the SSH key is not owned by default user account in docker, please also do "chmod 644 id_rsa.pub; chmod 644 id_rsa" to grant read access for default user account.
> Users could also use "/usr/bin/ssh-keygen -t rsa -b 4096 -N '' -f ~/mnt/ssh_key/id_rsa" to generate a new SSH Key inside the container.
> Users need to mount a config file to list all hostnames at location `/root/.ssh/config` on the SSH client container.
> Once all files are added

#### Setup and Run IPEX Multi-Node Container

Some additional assembly is required to utilize this container with OpenSSH. To perform any kind of DDP (Distributed Data Parallel) execution, containers are assigned the roles of launcher and worker respectively:

SSH Server (Worker)

1. *Authorized Keys* : `/etc/ssh/authorized_keys`

SSH Client (Launcher)

1. *Config File with Host IPs* : `/root/.ssh/config`
2. *Private User Key* : `/root/.ssh/id_rsa`

To add these files correctly please follow the steps described below.

1. Setup ID Keys

    You can use the commands provided below to [generate the Identity keys](https://www.ssh.com/academy/ssh/keygen#creating-an-ssh-key-pair-for-user-authentication) for OpenSSH.

    ```bash
    ssh-keygen -q -N "" -t rsa -b 4096 -f ./id_rsa
    touch authorized_keys
    cat id_rsa.pub >> authorized_keys
    ```

2. Add hosts to config

    The launcher container needs to have the a config file with all hostnames and ports specified. An example of a hostfile is provided below.

    ```bash
    touch config
    ```

    ```txt
    Host host1
        HostName <Hostname of host1>
        IdentitiesOnly yes
        Port <SSH Port>
    Host host2
        HostName <Hostname of host2>
        IdentitiesOnly yes
        Port <SSH Port>
    ...
    ```

3. Configure the permissions and ownership for all of the files you have created so far.

    ```bash
    chmod 600 id_rsa.pub id_rsa config authorized_keys
    chown root:root id_rsa.pub id_rsa config authorized_keys
    ```

4. Now start the workers and execute DDP on the launcher.

    1. Worker run command:

        ```bash
        export SSH_PORT=<SSH Port>
        docker run -it --rm \
            --net=host \
            -v $PWD/authorized_keys:/root/.ssh/authorized_keys \
            -v $PWD/tests:/workspace/tests \
            -w /workspace \
            -e SSH_PORT=${SSH_PORT} \
            intel/intel-extension-for-pytorch:2.3.0-pip-multinode \
            bash -c '/usr/sbin/sshd -D -p ${SSH_PORT} -f /var/run/sshd_config'
        ```

    2. Launcher run command:

        ```bash
        docker run -it --rm \
            --net=host \
            -v $PWD/id_rsa:/root/.ssh/id_rsa \
            -v $PWD/config:/root/.ssh/config \
            -v $PWD/tests:/workspace/tests \
            -w /workspace \
            -e SSH_PORT=${SSH_PORT} \
            intel/intel-extension-for-pytorch:2.3.0-pip-multinode \
            bash -c 'ipexrun cpu /workspace/tests/ipex-resnet50.py --ipex --device cpu --backend ccl'
        ```

> [!NOTE]
> [Intel MPI](https://www.intel.com/content/www/us/en/developer/tools/oneapi/mpi-library.html) can be configured based on your machine settings. If the above commands do not work for you, see the documentation for how to configure based on your network.

---

The images below are [TorchServe*] with CPU Optimizations:

| Tag(s)              | Pytorch  | IPEX         | Dockerfile      |
| ------------------- | -------- | ------------ | --------------- |
| `2.3.0-serving-cpu` | [v2.3.0] | [v2.3.0+cpu] | [v0.4.0-Beta]   |
| `2.2.0-serving-cpu` | [v2.2.0] | [v2.2.0+cpu] | [v0.3.4]        |

For more details, follow the procedure in the [TorchServe](https://github.com/pytorch/serve/blob/master/examples/intel_extension_for_pytorch/README.md) instructions.

## CPU only images with Intel® Distribution for Python*

The images below are built only with CPU optimizations (GPU acceleration support was deliberately excluded) and include [Intel® Distribution for Python*]:

| Tag(s)           | Pytorch  | IPEX         | Dockerfile      |
| ---------------- | -------- | ------------ | --------------- |
| `2.3.0-idp-base` | [v2.3.0] | [v2.3.0+cpu] | [v0.4.0-Beta]   |
| `2.2.0-idp-base` | [v2.2.0] | [v2.2.0+cpu] | [v0.3.4]        |
| `2.1.0-idp-base` | [v2.1.0] | [v2.1.0+cpu] | [v0.2.3]        |
| `2.0.0-idp-base` | [v2.0.0] | [v2.0.0+cpu] | [v0.1.0]        |

The images below additionally include [Jupyter Notebook](https://jupyter.org/) server:

| Tag(s)              | Pytorch  | IPEX         | Dockerfile      |
| ------------------- | -------- | ------------ | --------------- |
| `2.3.0-idp-jupyter` | [v2.3.0] | [v2.3.0+cpu] | [v0.4.0-Beta]   |
| `2.2.0-idp-jupyter` | [v2.2.0] | [v2.2.0+cpu] | [v0.3.4]        |
| `2.1.0-idp-jupyter` | [v2.1.0] | [v2.1.0+cpu] | [v0.2.3]        |
| `2.0.0-idp-jupyter` | [v2.0.0] | [v2.0.0+cpu] | [v0.1.0]        |

The images below additionally include [Intel® oneAPI Collective Communications Library] (oneCCL) and Neural Compressor ([INC]):

| Tag(s)                | Pytorch  | IPEX         | oneCCL               | INC       | Dockerfile      |
| --------------------- | -------- | ------------ | -------------------- | --------- | --------------- |
| `2.3.0-idp-multinode` | [v2.3.0] | [v2.3.0+cpu] | [v2.3.0][ccl-v2.3.0] | [v2.5.1]  | [v0.4.0-Beta]   |
| `2.2.0-idp-multinode` | [v2.2.0] | [v2.2.0+cpu] | [v2.2.0][ccl-v2.2.0] | [v2.4.1]  | [v0.3.4]        |
| `2.1.0-idp-mulitnode` | [v2.1.0] | [v2.1.0+cpu] | [v2.1.0][ccl-v2.1.0] | [v2.3.1]  | [v0.2.3]        |
| `2.0.0-idp-multinode` | [v2.0.0] | [v2.0.0+cpu] | [v2.0.0][ccl-v2.0.0] | [v2.1.1]  | [v0.1.0]        |

## Build from Source

To build the images from source, clone the [Intel® AI Containers](https://github.com/intel/ai-containers) repository, follow the main `README.md` file to setup your environment, and run the following command:

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

## License

View the [License](https://github.com/intel/intel-extension-for-pytorch/blob/main/LICENSE) for the [Intel® Extension for PyTorch*].

The images below also contain other software which may be under other licenses (such as Pytorch*, Jupyter*, Bash, etc. from the base).

It is the image user's responsibility to ensure that any use of The images below comply with any relevant licenses for all software contained within.

\* Other names and brands may be claimed as the property of others.

<!--Below are links used in these document. They are not rendered: -->

[Intel® Arc™ A-Series Graphics]: https://ark.intel.com/content/www/us/en/ark/products/series/227957/intel-arc-a-series-graphics.html
[Intel® Data Center GPU Flex Series]: https://ark.intel.com/content/www/us/en/ark/products/series/230021/intel-data-center-gpu-flex-series.html
[Intel® Data Center GPU Max Series]: https://ark.intel.com/content/www/us/en/ark/products/series/232874/intel-data-center-gpu-max-series.html

[Intel® Extension for PyTorch*]: https://intel.github.io/intel-extension-for-pytorch/
[Intel® Distribution for Python*]: https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-for-python.html
[Intel® oneAPI Collective Communications Library]: https://www.intel.com/content/www/us/en/developer/tools/oneapi/oneccl.html
[INC]: https://github.com/intel/neural-compressor
[PyTorch*]: https://pytorch.org/
[TorchServe*]: https://github.com/pytorch/serve

[v0.4.0-Beta]: https://github.com/intel/ai-containers/blob/main/pytorch/Dockerfile
[v0.3.4]: https://github.com/intel/ai-containers/blob/v0.3.4/pytorch/Dockerfile
[v0.2.3]: https://github.com/intel/ai-containers/blob/v0.2.3/pytorch/Dockerfile
[v0.1.0]: https://github.com/intel/ai-containers/blob/v0.1.0/pytorch/Dockerfile

[v2.1.30+xpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.1.30%2Bxpu
[v2.1.20+xpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.1.20%2Bxpu
[v2.1.10+xpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.1.10%2Bxpu
[v2.0.110+xpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.0.110%2Bxpu

[v2.3.0]: https://github.com/pytorch/pytorch/releases/tag/v2.3.0
[v2.2.0]: https://github.com/pytorch/pytorch/releases/tag/v2.2.0
[v2.1.0]: https://github.com/pytorch/pytorch/releases/tag/v2.1.0
[v2.0.1]: https://github.com/pytorch/pytorch/releases/tag/v2.0.1
[v2.0.0]: https://github.com/pytorch/pytorch/releases/tag/v2.0.0

[v2.5.1]: https://github.com/intel/neural-compressor/releases/tag/v2.5.1
[v2.4.1]: https://github.com/intel/neural-compressor/releases/tag/v2.4.1
[v2.3.1]: https://github.com/intel/neural-compressor/releases/tag/v2.3.1
[v2.1.1]: https://github.com/intel/neural-compressor/releases/tag/v2.1.1

[v2.3.0+cpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.3.0%2Bcpu
[v2.2.0+cpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.2.0%2Bcpu
[v2.1.0+cpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.1.0%2Bcpu
[v2.0.0+cpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.0.0%2Bcpu

[ccl-v2.3.0]: https://github.com/intel/torch-ccl/releases/tag/v2.3.0%2Bcpu
[ccl-v2.2.0]: https://github.com/intel/torch-ccl/releases/tag/v2.2.0%2Bcpu
[ccl-v2.1.0]: https://github.com/intel/torch-ccl/releases/tag/v2.1.0%2Bcpu
[ccl-v2.0.0]: https://github.com/intel/torch-ccl/releases/tag/v2.1.0%2Bcpu

[803]: https://dgpu-docs.intel.com/releases/LTS_803.29_20240131.html
[736]: https://dgpu-docs.intel.com/releases/stable_736_25_20231031.html
[647]: https://dgpu-docs.intel.com/releases/stable_647_21_20230714.html
