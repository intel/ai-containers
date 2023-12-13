# Intel® Tensorflow Distributed Execution in Containers
The Deep learning Intel® AI Tools Selector Preset Containers can be used to execute multi-node [Tensorflow](https://www.tensorflow.org) workloads using [Intel® Extension for Tensorflow](https://github.com/intel/intel-extension-for-tensorflow), [Intel® MPI](https://www.intel.com/content/www/us/en/developer/tools/oneapi/mpi-library.html) and [horovod](https://horovod.ai/). In this tutorial we use the [`horovodrun`](https://horovod.readthedocs.io/en/stable/running_include.html) utility to execute a [simple script](https://github.com/horovod/horovod/blob/master/examples/tensorflow2/tensorflow2_keras_mnist.py) that trains MNIST on multiple node. Here we use the Intel® AI Tools Selector Preset Container for Deep Learning to demonstrate the distributed workflow in a Tensorflow environment.

## Overall Workflow
To execute a script on multiple nodes using `horovorun` a basic understanding of the workflow is needed. When a script is launched using the `horovodrun` utility Horovod uses SSH to launch the script on multiple nodes defined in the command's parameter. SSH also provides the means for secure communication between the nodes. Horovod uses a backend for processes to create and pass messages among themselves effectively. In our case [Intel-MPI](https://www.intel.com/content/www/us/en/developer/tools/oneapi/mpi-library.html) is used as the backend. To start the workflow, a node is selected as *launcher node*, and the rest of the nodes are selected as *worker nodes*. All *worker nodes* first start the container with SSH daemon to be able to wait for the *launcher node* to make a connection to them. Then the container on the *launcher node* uses `horovodrun` to establish a connection with *worker nodes* and launch the script.

Before starting the workflow some prerequisites should be met which is described in the following [section](#prerequisites).

## Prerequisites
Following are the prerequisites before starting with distributed execution on Intel® TensorFlow containers
* Make sure all nodes can communicate with each other using networking. One way to check this is to use the `ping` utility to test the connection.
* SSH is set up correctly to communicate securely between the containers. Instructions to setup SSH correctly with the container are provided in [Setup SSH](#setup-ssh)
* If you want to run the workload on GPU machine, please make sure you've installed correct drivers on all nodes. You can follow the instructions provided [here](https://dgpu-docs.intel.com/driver/installation.html) to install the stable drivers.

## Setup

### Setup SSH
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

### Download the test script

For this experiment we're using an [example script](https://github.com/horovod/horovod/blob/master/examples/tensorflow2/tensorflow2_keras_mnist.py) from horovod. Use the following command to download the script.

```bash
mkdir -p workload
wget -O workload/tensorflow2_keras_mnist.py https://raw.githubusercontent.com/intel/intel-optimization-for-horovod/main/xpu_examples/tensorflow2/tensorflow2_keras_mnist.py
```

### Copy Files in corresponding nodes
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

## Run containers
Once the [prerequisites](#prerequisites) have been met and the [setup](#setup) has been completed, following commands(in order) can be used to launch the script on all nodes. In the following example, 2 instances are launched of a script: 1 on the launcher node(localhost) and 1 on a worker node. You can run the workload on [Intel® Flex/Max GPUs](https://www.intel.com/content/www/us/en/products/details/discrete-gpus/data-center-gpu.html) or [Intel® CPUs](https://www.intel.com/content/www/us/en/products/details/processors.html). Please follow instructions in [GPU section](#run-on-intel®-flexmax-gpus-machines) for running the workload on Intel® Flex/Max GPUs and [CPU section](#run-on-intel®-cpus-machines) for running the workload on Intel® CPUs.

### Run on [Intel® Flex/Max GPUs](https://www.intel.com/content/www/us/en/products/details/discrete-gpus/data-center-gpu.html) machines

>**Note:** Before you run on the GPUs you need to make sure the drivers are installed correctly on all nodes. Please follow the instructions provided [here](https://dgpu-docs.intel.com/driver/installation.html) to install the drivers.

* ### Run on worker nodes

    Please, run the following commands on all worker nodes in a shell to launch the container with ssh daemon.
    * Find your machine's `RENDER` and `VIDEO` group values to enable [Intel® Flex/Max GPU](https://www.intel.com/content/www/us/en/products/details/discrete-gpus/data-center-gpu.html).

        ```bash
        RENDER=$(getent group render | sed -E 's,^render:[^:]*:([^:]*):.*$,\1,')
        VIDEO=$(getent group video | sed -E 's,^video:[^:]*:([^:]*):.*$,\1,')
        test -z "$RENDER" || RENDER_GROUP="--group-add ${RENDER}"
        test -z "$VIDEO" || VIDEO_GROUP="--group-add ${VIDEO}"
        ```
    * Start the OpenSSH server inside the docker container.

        ```bash
        docker run --rm \
            ${RENDER_GROUP} \
            ${VIDEO_GROUP} \
            --device=/dev/dri \
            -v /dev/dri/by-path:/dev/dri/by-path \
            -v $PWD/workload:/tests \
            -v $PWD/ssh_worker:/home/dev/.ssh/ \
            --name=worker \
            --network=host  \
            -w /tests intel/deep-learning:2024.0-py3.10 \
            bash -c '/usr/sbin/sshd -p 12345 -f ~/.ssh/sshd_config -E ~/.ssh/error.log && sleep infinity'
        ```
>**Note:** that some parameters to the sshd utility need to be modified based on your configuration. For example, you might want to modify the `-p`(port) parameter to specify a different port if 12345 is not available. You can find out more options available to the SSH Daemon [here](https://www.ssh.com/academy/ssh/sshd#command-line-options).

* ### Run on launcher nodes

    Run the following command on the launcher nodes in a shell to launch the container with `mpirun` command.
    * Find your machine's `RENDER` and `VIDEO` group values to enable [Intel® Flex/Max GPU](https://www.intel.com/content/www/us/en/products/details/discrete-gpus/data-center-gpu.html).

        ```bash
        RENDER=$(getent group render | sed -E 's,^render:[^:]*:([^:]*):.*$,\1,')
        VIDEO=$(getent group video | sed -E 's,^video:[^:]*:([^:]*):.*$,\1,')
        test -z "$RENDER" || RENDER_GROUP="--group-add ${RENDER}"
        test -z "$VIDEO" || VIDEO_GROUP="--group-add ${VIDEO}"
        ```

    * Launch MNIST training script on all nodes using `horovodrun`.
    ```bash
    docker run --rm -t \
        ${RENDER_GROUP} \
        ${VIDEO_GROUP} \
        --device=/dev/dri \
        -v /dev/dri/by-path:/dev/dri/by-path \
        -v $PWD/workload:/tests \
        -v $PWD/ssh_launcher:/home/dev/.ssh/ \
        --name=launcher \
        --network=host  \
        -w /tests intel/deep-learning:2024.0-py3.10 \
        conda run --no-capture-output \
            -n tensorflow horovodrun --verbose \
            -np 2 \
            -H localhost:1,worker:1 \
            python tensorflow2_keras_mnist.py

### Run on [Intel® CPUs](https://www.intel.com/content/www/us/en/products/details/processors.html) machines

* ### Run on worker nodes

    Please, run the following command on all worker nodes in a shell to launch the container with ssh daemon.

    ```bash
    docker run --rm \
        -v $PWD/workload:/tests \
        -v $PWD/ssh_worker:/home/dev/.ssh/ \
        --name=worker \
        --network=host  \
        -w /tests intel/deep-learning:2024.0-py3.10 \
        bash -c '/usr/sbin/sshd -p 12345 -f ~/.ssh/sshd_config -E ~/.ssh/error.log && sleep infinity'
    ```

>**Note:** that some parameters to the sshd utility need to be modified based on your configuration. For example, you might want to modify the `-p`(port) parameter to specify a different port if 12345 is not available. You can find out more options available to the SSH Daemon [here](https://www.ssh.com/academy/ssh/sshd#command-line-options).

* ### Run on launcher nodes

    Please, run the following command on the launcher nodes in a shell to launch the container with `horovrun` command.

    ```bash
    docker run --rm -t \
        -v $PWD/workload:/tests \
        -v $PWD/ssh_launcher:/home/dev/.ssh/ \
        --name=launcher \
        --network=host  \
        -w /tests intel/deep-learning:2024.0-py3.10 \
        conda run --no-capture-output \
            -n tensorflow horovodrun --verbose \
            -np 2 \
            -H localhost:1,worker:1 \
            python tensorflow2_keras_mnist.py
    ```
>**Note:** that the number of processes spawned on each node will be dependent on the parameters specified with `horovodrun` command. You can modify the horovodrun command to your needs from the [documentation here](https://horovod.readthedocs.io/en/stable/running_include.html) and [here](https://horovod.readthedocs.io/en/stable/docker_include.html). For the workflow to work all nodes need to communicate with each other and be able to pass the MPI messages among all processes.  This requires the correct envrionment setup based on the specific networking setup you have. [Intel® MPI documentation](https://www.intel.com/content/www/us/en/docs/mpi-library/developer-reference-linux/2021-10/environment-variable-reference.html) provides the necessary environment variables to control the communication between processes using MPI.
