# PyTorch Ingredients

## PyTorch

### Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| BASE_IMAGE_NAME | `ubuntu` | Base Operating System |
| BASE_IMAGE_TAG | `22.04` | Base Operating System Version |
| IDP_VERSION | `core` | Intel Distribution of Python version(either `full` or `core`) |
| IPEX_VERSION | `2.1.0` | Intel Extension for PyTorch Version |
| MINICONDA_VERSION | `latest-Linux-x86_64` | Miniconda Version from `https://repo.anaconda.com/miniconda` |
| PACKAGE_OPTION | `pip` | Stock Python (pypi) or Intel Python (conda) (`pip` or `idp`) |
| PYTHON_VERSION | `3.10` | Python Version |
| PYTORCH_VERSION | `2.1.0+cpu` | PyTorch Version |
| TORCHAUDIO_VERSION | `2.1.0+cpu` | TorchAudio Version |
| TORCHVISION_VERSION | `0.16.0+cpu` | TorchVision Version |

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
| INC_VERSION | `2.3.1` | Neural Compressor Version |
| ONECCL_VERSION | `2.1.0+cpu` | TorchCCL Version |

### IPEX XPU Base

Built from Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| ICD_VER | `23.17.26241.33-647~22.04` | OpenCL Version |
| LEVEL_ZERO_GPU_VER | `1.3.26241.33-647~22.04` | Level Zero GPU Version |
| LEVEL_ZERO_VER | `1.11.0-647~22.04` | Level Zero Version |
| DPCPP_VER | `2023.2.1-16` | DPCPP Version | 
| MKL Version | `2023.2.0-49495` | MKL Version |
| CCL_VER | `2021.10.0-49084` | CCL Version |
| TORCH_VERSION | `2.0.1a0+cxx11.abi` | Torch Version |
| TORCHVISION_VERSION | `0.15.2a0+cxx11.abi` | Torchvision Version |
| IPEX_VERSION | `2.0.110+xpu` | IPEX Version |
| TORCH_WHL_URL | `https://developer.intel.com/ipex-whl-stable-xpu` | Wheel URL |
| ONECCL_BIND_PT_VERSION | `2.0.100` | TorchCCL Version | 

### IPEX XPU Jupyter

Built from IPEX XPU Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| PORT | `8888` | Server UI Port |

### Intel® PyTorch Distributed Execution in Containers
The Deep learning Intel® AI Tools Selector Preset Containers can be used to execute multi-node [PyTorch](https://www.pytorch.org) workloads using [Intel® Extension for PyTorch](https://github.com/intel/intel-extension-for-pytorch) and [Intel® OneCCL](https://www.intel.com/content/www/us/en/developer/tools/oneapi/oneccl.html). In this tutorial we use the [`ipexrun`](https://intel.github.io/intel-extension-for-pytorch/latest/tutorials/performance_tuning/launch_script.html) utility to execute a [simple script](https://github.com/kubeflow/training-operator/blob/master/examples/pytorch/mnist/mnist.py) that trains MNIST on multiple node. Here we use the Intel® AI Tools Selector Preset Container for Deep Learning to demonstrate the distributed workflow in a PyTorch environment.

#### Overall Workflow
To execute a script on multiple nodes using `ipexrun` a basic understanding of the workflow is needed. When a script is launched using the `ipexrun` utility IPEX uses SSH to launch the script on multiple nodes defined in the command's parameter. SSH also provides the means for secure communication between the nodes. IPEX uses a backend for processes to create and pass messages among themselves effectively. In our case [OneCCL](https://www.intel.com/content/www/us/en/developer/tools/oneapi/oneccl.html) is used as the backend. To start the workflow, a node is selected as *launcher node*, and
 the rest of the nodes are selected as *worker nodes*. All *worker nodes* first start the container with SSH daemon to be able to wait for the *launcher node* to make a connection to them. Then the container on the *launcher node* uses `ipexrun` to establish a connection with *worker nodes* and launch the script.

Before starting the workflow some prerequisites should be met which is described in the following [section](#prerequisites).

**Note:** Torch uses the term `master` for the launcher host, so some parameters and environment variables will contain it instead of `launcher`.

#### Prerequisites
Following are the prerequisites before starting with distributed execution on Intel® PyTorch containers
* Make sure all nodes can communicate with each other using networking. 
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

* The launcher node needs to have the a config file with all hostnames specified. An example of a hostfile is provided below. Please add the worker nodes and launcher nodes' IP and the corresponding ports for SSH to use.

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

For this experiment we're using an [example script](https://github.com/kubeflow/training-operator/blob/master/examples/pytorch/mnist/mnist.py). Use the following command to download the script.

    ```bash
    mkdir -p workload
    wget -O workload/pytorch_mnist.py https://raw.githubusercontent.com/kubeflow/training-operator/master/examples/pytorch/mnist/mnist.py
    sed -i 's|\.\./data|./data|' workload/pytorch_mnist.py #little change required to run with this example
    ```

##### Create hostfile with the involved hosts
A plain text file should be created to let the `ipexrun` command find the worker hosts. The first line is the launcher host IP Address, then every subsequent line should contain the host names as listed in the Host entries in SSH config file created previously.

    ```bash
    echo <launcher_ip_address> > workload/hostfile
    echo <worker1_Host_value> >> workload/hostfile
    echo <worker2_Host_value> >> workload/hostfile
    ...
    ```

An example `hostfile` might look like this:

    ```
    10.0.0.5
    worker1
    worker2
    ...
    ```

##### Copy Files in corresponding nodes
* Copy the `ssh_worker` and `workload` directories to all worker nodes, and the `ssh_launcher` and `workload` directories to the launcher node.

* The default user in the container is `dev` with user ID `1000`. Correct permissions need to be set for files to use the SSH as a user in the container. Use the following commands on every worker node and the launcher node to change the permissions to the correct ones.

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
    IMAGE_NAME=intel/deep-learning:2024.0-py3.9
    docker run --rm \
      -v $PWD/workload:/tests \
      -v $PWD/ssh_worker:/home/dev/.ssh/ \
      --name=worker \
      --network=host  \
      -e MASTER_ADDR=<launcher_ip_address> \
      -e MASTER_PORT=<any_free_port_in_the_host_to_use> \
      -w /tests $IMAGE_NAME \
      bash -c '/usr/sbin/sshd -p 12345 -f ~/.ssh/sshd_config -E ~/.ssh/error.log && sleep infinity'
    ```

>**Note:** that some parameters to the sshd utility need to be modified based on your configuration. For example, you might want to modify the `-p`(port) parameter to specify a different port if 12345 is not available. You can find out more options available to the SSH Daemon [here](https://www.ssh.com/academy/ssh/sshd#command-line-options).

* ##### Run on launcher nodes

    Run the following command on the launcher nodes in a shell to launch the container with `ipexrun` command.

    ```bash
    IMAGE_NAME=intel/deep-learning:2024.0-py3.9
    docker run --rm \
      -v $PWD:/tests \
      -v $PWD/client:/home/dev/.ssh/ \
      --name=launcher \
      --network=host \
      -e MASTER_ADDR=<launcher_ip_address> \
      -e MASTER_PORT=<any_free_port_in_the_host_to_use> \
      -w /tests/workdir \
      --shm-size 8GB \
      -it $IMAGE_NAME bash -c \
      conda run --no-capture-output \
        -n torch-cpu ipexrun --distributed \
        --nproc_per_node=2 --nnodes=2 \
        --hostfile hostfile \
        pytorch_mnist.py --no-cuda --save-model
    ```

>**Note:** that the number of processes spawned on each node will be dependent on the parameters specified with `ipexrun` command. You can modify the ipexrun command to your needs from the [documentation here](https://intel.github.io/intel-extension-for-pytorch/latest/tutorials/performance_tuning/launch_script.html) and [here](https://github.com/intel/intel-extension-for-pytorch). For the workflow to work all nodes need to communicate with each other and be able to pass the OneCCL messages among all processes.  This requires the correct envrionment setup based on the specific networking setup you have. [Intel® OneCCL](https://www.intel.com/content/www/us/en/developer/tools/oneapi/oneccl.html) provides the necessary environment variables to control the communication between processes using OneCCL.

* ##### Running on VMware hosts

The Docker Run command may need to be modified to account for a different network interface, if that interface is not default and is used for communication between VMs. Below are some arguments that can be appended to the docker run commands shown above to ensure that IMPI uses the correct interface when communicating between nodes.

    ```
    -e I_MPI_HYDRA_IFACE="<network_interface_to_use>" #e.g. "eth0"\
    -e FI_SOCKETS_IFACE=<network_interface_to_use> \
    -e FI_TCP_IFACE=<network_interface_to_use> \
    -e UCX_TLS=all \
    ```

#### Distributed Training on k8s

Use _N_-Nodes in your Training with PyTorchJobs and Kubeflow's Training Operator with an optimized production container.

##### Distributed Production Container

Create a Distributed Production Container using Intel Optimized PyTorch MultiNode layers. For Example:

```dockerfile
# Add Some Multinode image layers
FROM intel/intel-optimized-pytorch:2.1.0-pip-multinode as prod-base
# Use an existing container target
FROM base as prod

# Copy in Intel Optimized PyTorch MultiNode python environment, this will overwrite any packages with the same name
COPY --from=prod-base /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.10/dist-packages
COPY --from=prod-base /usr/local/bin /usr/local/bin

...
```

##### Build the Container with New Stage

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

Configure the Helm Chart by changing [pytorchjob](chart/templates/pytorchjob.yaml#L18-L46), [pvc](chart/templates/pvc.yaml), and [values](chart/values.yaml) files.

Afterwards, deploy to the cluster with `helm install`. To see all of the options, see the [README](chart/README.md) for the chart.

```bash
export NAMESPACE=kubeflow
helm install ---namespace ${NAMESPACE} \
     --set metadata.name=<workflow-name> \
     --set metadata.namespace=<namespace with training operator> \
     --set imageName=<Docker Image repository/Name> \
     --set imageTag=<Docker Image Tag> \
     ...
     ipex-distributed
     ./chart
```

To see an existing configuration utilizing this method, check out [Intel® Extension for Transformers](https://github.com/intel/intel-extension-for-transformers/blob/main/docker/README.md#kubernetes)' implementation.

##### Troubleshooting

- [TorchCCL Reference](https://github.com/intel/torch-ccl)
- [PyTorchJob Reference](https://www.kubeflow.org/docs/components/training/pytorch/)
- [Training Operator Reference](https://github.com/kubeflow/training-operator)
- When applying proxies specify all of your proxies in a configmap in the same namespace, and add the following to both your launcher and workers:

```yaml
envFrom:
  - configMapRef:
      name: my-proxy-configmap-name
```
