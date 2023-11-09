# TensorFlow Ingredients

## TensorFlow

### Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| BASE_IMAGE_NAME | `ubuntu` | Base Operating System |
| BASE_IMAGE_TAG | `22.04` | Base Operating System Version |
| IDP_VERSION | `core` | Intel Distribution of Python version(either `full` or `core`) |
| MINICONDA_VERSION | `latest-Linux-x86_64` | Miniconda Version from `https://repo.anaconda.com/miniconda` |
| PACKAGE_OPTION | `pip` | Stock Python (pypi) or Intel Python (conda) (`pip` or `idp`) |
| PYTHON_VERSION | `3.10` | Python Version |
| TF_PACKAGE | `intel-tensorflow` | TF Package (`tensorflow`, `intel-tensorflow`, `intel-tensorflow-avx512`) |
| TF_PACKAGE_VERSION | `2.12.0` | TensorFlow Version |

### Jupyter

Built from Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| PORT | `8888` | Server UI Port |

### MLFlow

Built from Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| PORT | `5000` | Server UI Port |

### MultiNode

Built from Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| HOROVOD_VERSION | `0.28.0` | Horovod Version |
| INC_VERSION | `2.1.1` | Neural Compressor Version |
| MPI | `openmpi` | MPI Installation type (`openmpi` or `mpich`) |

### ITEX XPU Base

Built from Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| ICD_VER | `23.17.26241.33-647~22.04` | OpenCL Version |
| LEVEL_ZERO_GPU_VER | `1.3.26241.33-647~22.04` | Level Zero GPU Version |
| LEVEL_ZERO_VER | `1.11.0-647~22.04` | Level Zero Version |
| DPCPP_VER | `2023.2.1-16` | DPCPP Version | 
| MKL Version | `2023.2.0-49495` | MKL Version |
| CCL_VER | `2021.10.0-49084` | CCL Version |
| TF_VERSION | `2.13` | TensorFlow Version |

### ITEX XPU Jupyter

Built from ITEX XPU Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| PORT | `8888` | Server UI Port |

### Intel® Tensorflow Distributed Execution in Containers
The Deep learning Intel® AI Tools Selector Preset Containers can be used to execute multi-node [Tensorflow](https://www.tensorflow.org) workloads using [Intel® Extension for Tensorflow](https://github.com/intel/intel-extension-for-tensorflow), [Intel® MPI](https://www.intel.com/content/www/us/en/developer/tools/oneapi/mpi-library.html) and [horovod](https://horovod.ai/). In this tutorial we use the [`horovodrun`](https://horovod.readthedocs.io/en/stable/running_include.html) utility to execute a [simple script](https://github.com/horovod/horovod/blob/master/examples/tensorflow2/tensorflow2_keras_mnist.py) that trains MNIST on multiple node. Here we use the Intel® AI Tools Selector Preset Container for Deep Learning to demonstrate the distributed workflow in a Tensorflow environment.

#### Overall Workflow
To execute a script on multiple nodes using `horovorun` a basic understanding of the workflow is needed. When a script is launched using the `horovodrun` utility Horovod uses SSH to launch the script on multiple nodes defined in the command's parameter. SSH also provides the means for secure communication between the nodes. Horovod uses a backend for processes to create and pass messages among themselves effectively. In our case [Intel-MPI](https://www.intel.com/content/www/us/en/developer/tools/oneapi/mpi-library.html) is used as the backend. To start the workflow, a node is selected as *launcher node*, and
 the rest of the nodes are selected as *worker nodes*. All *worker nodes* first start the container with SSH daemon to be able to wait for the *launcher node* to make a connection to them. Then the container on the *launcher node* uses `horovodrun` to establish a connection with *worker nodes* and launch the script.

Before starting the workflow some prerequisites should be met which is described in the following [section](#prerequisites).

#### Prerequisites
Following are the prerequisites before starting with distributed execution on Intel® TensorFlow containers
* Make sure all nodes can communicate with each other using networking. One way to check this is to use the `ping` utility to test the connection.
* SSH is set up correctly to communicate securely between the containers. Instructions to setup SSH correctly with the container are provided in [Setup SSH](#setup-ssh)

#### Setup

##### Setup SSH
Before the containers are started on *worker nodes* or *launcher nodes* some files are needed to enable the SSH server and client inside the containers. The following steps can be used to set up SSH correctly.


* Run the following command to create directories to setup SSH for each container.

    ```bash
    mkdir -p ssh_launcher
    mkdir -p ssh_worker
    ```

* You can use the commands provided below to [generate the Identity keys](https://www.ssh.com/academy/ssh/keygen#creating-an-ssh-key-pair-for-user-authentication) for OpenSSH. After this, you should have a public and private key which will be used for passwordless authentication. If you already have identity keys beforehand you can skip the ssh-keygen command and replace the public and private keys paths with your own in the copy commands.

    ```bash
    mkdir -p id_keys
    ssh-keygen -q -N "" -t rsa -b 4096 -f id_keys/id_rsa
    cp id_keys/id_rsa.pub ssh_worker/authorized_keys #Private Key
    cp id_keys/id_rsa ssh_launcher/ #Public Key
    ```

* You can use the commands provided below to [generate the host keys](https://www.ssh.com/academy/ssh/keygen#creating-host-keys) for OpenSSH. After this you should have host keys which will be used for communicating with the host machines on the respective nodes. If you already have host keys beforehand you can skip the ssh-keygen command and replace the host keys paths with your own in the copy commands.

    ```bash
    mkdir -p host_keys/
    ssh-keygen -q -N "" -t dsa -f host_keys/ssh_host_dsa_key
    ssh-keygen -q -N "" -t rsa -b 4096 -f host_keys/ssh_host_rsa_key
    ssh-keygen -q -N "" -t ecdsa -f host_keys/ssh_host_ecdsa_key
    ssh-keygen -q -N "" -t ed25519 -f host_keys/ssh_host_ed25519_key
    cp -r host_keys/* ssh_worker/
    ```

* To run SSH Daemon on worker nodes the configuration needs to be correct. Please, use the following command to save the sshd configuration.

    ```bash
    echo -e '## provide the new path containing these host keys

    HostKey ~/.ssh/ssh_host_dsa_key
    HostKey ~/.ssh/ssh_host_rsa_key
    HostKey ~/.ssh/ssh_host_ecdsa_key
    HostKey ~/.ssh/ssh_host_ed25519_key

    AuthorizedKeysFile ~/.ssh/authorized_keys
    ## Enable DEBUG log. You can ignore this but this may help you debug any issue while enabling SSHD for the first time
    LogLevel DEBUG3
    ChallengeResponseAuthentication no
    UsePAM yes
    PrintMotd no
    ## Provide a path to store PID file which is accessible by normal user for write purpose
    PidFile ~/.ssh/sshd.pid
    AcceptEnv LANG LC_*
    Subsystem       sftp    /usr/lib/openssh/sftp-server
    ' > ssh_worker/sshd_config
    ```

* The launcher node needs to have the correct config file with all hostnames specified. An example of a hostfile is provided below. Please add the worker nodes and launcher nodes' IP and the corresponding ports for SSH to use.

    ```
    Host launcher
        HostName <Hostname of launcher>
        IdentitiesOnly yes
        Port <Port x>
    Host worker1
        HostName <Hostname of worker1>
        IdentitiesOnly yes
        Port <Port y>
    Host worker2
        HostName <Hostname of worker2>
        IdentitiesOnly yes
        Port <Port z>
    ...

    ```
    Once the file is created you can copy it to the launcher node directory using the following command

    ```bash
    cp <path to config> ssh_launcher/config
    ```

##### Download the test script

For this experiment we're using an [example script](https://github.com/horovod/horovod/blob/master/examples/tensorflow2/tensorflow2_keras_mnist.py) from horovod. Use the following command to download the script.

    ```bash
    mkdir -p workload
    wget -O workload/tensorflow2_keras_mnist.py https://raw.githubusercontent.com/horovod/horovod/master/examples/tensorflow2/tensorflow2_keras_mnist.py
    ```

##### Copy Files in corresponding nodes
* Copy the `ssh_worker` directory to all worker nodes and the `ssh_launcher`, and `workload` directories to the launcher node.

* The default user in the container is `dev` with user ID `1000`. Correct permissions need to be set for files to use the SSH as a user in the container. The default user in the container is `dev` with user ID `1000`. Use the following commands on every worker node and the launcher node to change the permissions to the correct ones.

* Run the following command on all *worker nodes*.
    
    ```bash
    chown -R 1000:1000 ssh_worker workload #run this on all worker nodes
    ```

* Run the following command on the *launcher node*.

    ```bash
    chown -R 1000:1000 ssh_launcher workload #run this on the launcher node
    ```

#### Run containers
Once the [prerequisites](#prerequisites) have been met and the [setup](#setup) has been completed following commands(in order) can be used to launch the script on all nodes. In the following example, 2 instances are launched of a script: 1 on the launcher node(localhost) and 1 on a worker node.

* ##### Run on worker nodes

    Please, run the following command on all worker nodes in a shell to launch the container with ssh daemon.

    ```bash
    docker run --rm \
        -v $PWD/workload:/tests \
        -v $PWD/ssh_worker:/home/dev/.ssh/ \
        --name=worker \
        --network=host  \
        -w /tests intel/deep-learning:2023.2-py3.10 \
        bash -c '/usr/sbin/sshd -p 12345 -f ~/.ssh/sshd_config -E ~/.ssh/error.log && sleep infinity'
    ```

>**Note:** that some parameters to the sshd utility need to be modified based on your configuration. For example, you might want to modify the `-p`(port) parameter to specify a different port if 12345 is not available. You can find out more options available to the SSH Daemon [here](https://www.ssh.com/academy/ssh/sshd#command-line-options).

* ##### Run on launcher nodes

    Please, run the following command on the launcher nodes in a shell to launch the container with `horovrun` command.

    ```bash
    docker run --rm -t \
        -v $PWD/workload:/tests \
        -v $PWD/ssh_launcher:/home/dev/.ssh/ \
        --name=launcher \
        --network=host  \
        -w /tests intel/deep-learning:2023.2-py3.10 \
        conda run --no-capture-output \
            -n tensorflow horovodrun --verbose \
            -np 2 \
            -H localhost:1,worker:1 \
            python tensorflow2_keras_mnist.py
    ```
>**Note:** that the number of processes spawned on each node will be dependent on the parameters specified with `horovodrun` command. You can modify the horovodrun command to your needs from the [documentation here](https://horovod.readthedocs.io/en/stable/running_include.html) and [here](https://horovod.readthedocs.io/en/stable/docker_include.html). For the workflow to work all nodes need to communicate with each other and be able to pass the MPI messages among all processes.  This requires the correct envrionment setup based on the specific networking setup you have. [Intel® MPI documentation](https://www.intel.com/content/www/us/en/docs/mpi-library/developer-reference-linux/2021-10/environment-variable-reference.html) provides the necessary environment variables to control the communication between processes using MPI.

#### Distributed Training on k8s

Use _N_-Nodes in your Training with MPI Operator and an optimized production container.

##### Distributed Production Container

Create a Distributed Production Container using Intel Optimized TensorFlow MultiNode layers. For Example:

```dockerfile
# Add Some Multinode image layers
FROM intel/intel-optimized-tensorflow:2.12.0-pip-openmpi-multinode as prod-base
# Use an existing container target
FROM base as prod

# Copy in Intel Optimized TensorFlow MultiNode python environment, this will overwrite any packages with the same name
COPY --from=prod-base /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.10/dist-packages
COPY --from=prod-base /usr/local/bin /usr/local/bin

# Install MPI
RUN apt-get update -y && apt-get install -y --no-install-recommends --fix-missing \
    libopenmpi-dev \
    openmpi-bin \
    openmpi-common \
    openssh-client \
    openssh-server
...
```

##### Build the Container with New Stage

For a BKM on how to install MPI see the [MLOps Best Known Method](Dockerfile#L128).

```bash
docker build ... --target prod -t my_container:prod .
```

##### Configure Kubernetes

Using an existing Kubernetes Cluster of any flavor, install the standalone training operator from GitHub or use a pre-existing Kubeflow configuration.

```bash
kubectl apply -k "github.com/kubeflow/training-operator/manifests/overlays/standalone"
```

Ensure that the training operator deployment readiness status `1/1` before proceeding.

##### Deploy Distributed Job

Install [Helm](https://helm.sh/docs/intro/install/)

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 && \
chmod 700 get_helm.sh && \
./get_helm.sh
```

Configure the Helm Chart by changing [mpijob](chart/templates/mpijob.yaml#L28), [pvc](chart/templates/pvc.yaml), and [values](chart/values.yaml) files.

Afterwards, deploy to the cluster with `helm install`. To see all of the options, see the [README](chart/README.md) for the chart.

```bash
export NAMESPACE=kubeflow
helm install ---namespace ${NAMESPACE} \
     --set metadata.name=<workflow-name> \
     --set metadata.namespace=<namespace with training operator> \
     --set imageName=<Docker Image repository/Name> \
     --set imageTag=<Docker Image Tag> \
     --set slotsPerWorker=1 \
     ...
     itex-distributed
     ./chart
```

To see an existing configuration utilizing this method, check out [Intel® Transfer Learning Tool](https://github.com/IntelAI/transfer-learning/blob/main/docker/README.md#kubernetes)'s implementation.

##### Troubleshooting

- [Common Horovod Issues](https://horovod.readthedocs.io/en/stable/troubleshooting_include.html)
- [MPI Operator Reference](https://github.com/kubeflow/mpi-operator)
- [Training Operator Reference](https://github.com/kubeflow/training-operator)
- When applying proxies specify all of your proxies in a configmap in the same namespace, and add the following to both your launcher and workers:

```yaml
envFrom:
  - configMapRef:
      name: my-proxy-configmap-name
```

## TensorFlow Serving

### TF Serving

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| BASE_IMAGE_NAME | `ubuntu` | Base Operating System |
| BASE_IMAGE_TAG | `22.04` | Base Operating System Version |
| BAZEL_VERSION | `5.4.0` | Bazel Version |
| TF_PACKAGE | `intel-tensorflow` | TF Package (`tensorflow`, `intel-tensorflow`, `intel-tensorflow-avx512`) |
| TF_SERVING_BAZEL_OPTIONS | `'--local_ram_resources=HOST_RAM*0.8 --local_cpu_resources=HOST_CPUS-4'` | Bazel Options |
| TF_SERVING_BUILD_OPTIONS | `'--config=mkl --config=release --define=build_with_openmp=false --copt=-march=native'` | Serving Build Options |
| TF_SERVING_VERSION | `2.12.0` | TensorFlow Version |
| TF_SERVING_VERSION_GIT_BRANCH | `${TF_SERVING_VERSION}` | Branch/Ref for TF Serving Repository |

### Serving MKL

Built from TF Serving

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| BASE_IMAGE_NAME | `${TF_PACKAGE:-intel-tensorflow}-${BASE_IMAGE_NAME:-ubuntu}-${PACKAGE_OPTION:-pip}` | TF Serving Name |
| BASE_IMAGE_TAG | `serving` | TF Serving Tag |
| TF_SERVING_BUILD | `${BASE_IMAGE_NAME:-ubuntu}:${BASE_IMAGE_TAG:-22.04}` | Serving MKL OS `Base:Tag` |
| TF_SERVING_VERSION_GIT_COMMIT | `${TF_SERVING_VERSION}` | Commit/Branch/Ref for TF Serving Repository |
