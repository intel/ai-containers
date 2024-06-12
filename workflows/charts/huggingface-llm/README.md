# Fine Tune a Hugging Face LLM using a Kubernetes Cluster

In order to speed up the amount of time it takes to train a model using Intel® Xeon® Scalable Processors, multiple
machines can be used to distribute the workload. This guide will focus on using multiple nodes from a
[Kubernetes](https://kubernetes.io) cluster to fine tune Llama2. It uses the [meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
and [meta-llama/Llama-2-7b-hf](https://huggingface.co/meta-llama/Llama-2-7b-hf) pretrained models from
[Hugging Face Hub](https://huggingface.co), but similar large language models can be substituted into the same template.
The [PyTorch Training operator](https://www.kubeflow.org/docs/components/training/pytorch/) from
[Kubeflow](https://www.kubeflow.org) is used to deploy the distributed training job to the Kubernetes cluster. To
optimize the performance, [Intel® Extension for PyTorch](https://github.com/intel/intel-extension-for-pytorch) is used
during training and the [Intel® oneAPI Collective Communications Library (oneCCL)](https://github.com/oneapi-src/oneCCL)
is used as the DDP backend. The `intel/intel-optimized-pytorch:2.3.0-pip-multinode` base image already includes these
components, so that base image is used and other libraries like Hugging Face Transformers are added on to fine tune the
LLM.

## Requirements

Cluster requirements:

* Kubernetes cluster with Intel® Xeon® Scalable Processors
* [Kubeflow](https://www.kubeflow.org/docs/started/installing-kubeflow/) PyTorch Training operator deployed to the cluster
* NFS backed Kubernetes storage class

Client requirements:

* [kubectl command line tool](https://kubernetes.io/docs/tasks/tools/)
* [Helm command line tool](https://helm.sh/docs/intro/install/)
* Access to the [Llama 2 model in Hugging Face](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf) and a
  [Hugging Face token](https://huggingface.co/docs/hub/security-tokens). Alternatively, a similar LLM can be
  substituted.
* A clone of this repository (to access the helm chart files)

## Components

### Helm chart

A Helm chart is used to package the resources needed to run the distributed training job. The Helm chart in this
directory includes the following components:

* [PyTorchJob](templates/pytorchjob.yaml), which launches a pod for each worker
* [Kubernetes secret](templates/secret.yaml) with your Hugging Face token for authentication to access gated models
* [Persistent volume claim (PVC)](templates/pvc.yaml) to provides a storage space for saving checkpoints,
  saved model files, etc.
* [Data access pod](templates/dataaccess.yaml) is a dummy pod (running `sleep infinity`) with a volume mount to
  the PVC to allow copying files on and off of the volume. This pod can be used to copy datasets to the PVC before fine
  tuning or to download the fined tuned model after training completes.

The chart's [values.yaml](values.yaml) contains parameter values that get passed to the PyTorchJob and PVC specs
when the helm chart is installed or updated. The parameters include information about the resources being requested
to execute the job (such as the amount of CPU and memory resource, storage size, the number of workers, the types of
workers, etc) as well as parameters that are passed the the fine tuning python script such as the name of the
pretrained model, the dataset, learning rate, the number of training epochs, etc.

### Secret

Before using Llama 2 models you will need to [request access from Meta](https://ai.meta.com/resources/models-and-libraries/llama-downloads/)
and [get access to the model from HuggingFace](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf). For this reason,
authentication is required when fine tuning Llama 2 through the Kubernetes job. The helm chart includes a
[Kubernetes secret](https://kubernetes.io/docs/concepts/configuration/secret/) which gets populated with the encoded
Hugging Face token. The secret is mounted as a volume in the PyTorch Job containers using the `HF_HOME` directory to
authenticate your account to access gated models. If you want to run the fine tuning job with a non-gated model, you do
not need to provide a HF token in the Helm chart values file.

### Storage

A [persistent volume claim (PVC)](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) backed by a NFS
[Storage Class](https://kubernetes.io/docs/concepts/storage/storage-classes/) is used provide a common storage location
that is shared by the worker pods during training. The PVC is mounted as a volume in each container for the worker
pods. The volume is used to store the dataset, pretrained model, and checkpoint files during training. After training
completes, the trained model is written to the PVC, and if quantization is done, the quantized model will also be
saved to the volume.

### Container

The [Docker](https://www.docker.com) container used in this example includes all the dependencies needed to run
distributed PyTorch training using a Hugging Face model and a fine tuning script. This directory includes the
[`Dockerfile`](Dockerfile) that was used to build the container.

An image has been published to DockerHub (`intel/ai-workflows:torch-2.3.0-huggingface-multinode-py3.10`) with
the following major packages included:

| Package Name | Version | Purpose |
|--------------|---------|---------|
| [PyTorch](https://pytorch.org/) | 2.3.0+cpu | Base framework to train models |
| [Intel® Extension for PyTorch](https://github.com/intel/intel-extension-for-pytorch) | 2.3.0+cpu | Utilizes Intel®'s optimization |
| [Intel® Neural Compressor](https://github.com/intel/neural-compressor) | 2.4.1 | Optimize model for inference post-training |
| [Intel® oneAPI Collective Communications Library](https://github.com/oneapi-src/oneCCL) | 2.3.0+cpu | Deploy PyTorch jobs on multiple nodes |

See the [build from source instructions](../../../../tensorflow/README.md#build-from-source) to build a custom LLM fine
tuning container.

## Running the distributed training job

> Prior to running the examples, ensure that your Kubernetes cluster meets the
> [cluster requirements](#requirements) mentioned above.

Select a predefined use cases (such as fine tuning using the [Medical Meadow](https://github.com/kbressem/medAlpaca)
dataset), or use the template and fill in parameters to use your own workload. There are separate
[Helm chart values files](https://helm.sh/docs/chart_template_guide/values_files/) that can be used for each of these
usages:

| Value file name | Description |
|-----------------|-------------|
| [`values.yaml`](values.yaml) | Template for your own distributed fine tuning job. Fill in the fields for your workload and job parameters. |
| [`medical_meadow_values.yaml`](medical_meadow_values.yaml) | Helm chart values for fine tuning Llama 2 using the [Medical Meadow flashcards dataset](https://huggingface.co/datasets/medalpaca/medical_meadow_medical_flashcards) |
| [`financial_chatbot_values.yaml`](financial_chatbot_values.yaml) | Helm chart values for fine tuning Ll ama 2 using a subset of [Financial alpaca dataaset](https://huggingface.co/datasets/gbharti/finance-alpaca) as a custom dataset |

Pick one of the value files to use depending on your desired use case, and then follow the instructions below to
fine tune the model.

### Helm chart values table

<details>
  <summary> Expand to see the values table </summary>

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| deploy.env.configMapName | string | `nil` |  |
| deploy.env.enabled | bool | `false` |  |
| distributed.benchmark.coresPerInstance | int | `-1` | When benchmarking is enabled, the number of CPU cores to use per instance |
| distributed.benchmark.iterations | int | `300` | When benchmarking is enabled, the number of iterations to run performance tests |
| distributed.benchmark.numInstances | int | `1` | When benchmarking is enabled, the number of instances to use for performance testing. |
| distributed.benchmark.warmup | int | `30` | When benchmarking is enabled, the number of iterations to warmup before running performance tests. |
| distributed.doBenchmark | bool | `false` | If set to true, the Intel Neural Compressor will be used to benchmark the trained model. If the model is being quantized, the quantized model will also be benchmarked. |
| distributed.doEval | bool | `true` | If set to true, evaluation will be run with the validation split of the dataset, using the Hugging Face Transformers library. |
| distributed.doQuantize | bool | `false` | If set to true, the Intel Neural Compressor will be used to quantize the trained model. |
| distributed.doTrain | bool | `true` | If set to true, training will be run using the Hugging Face Transformers library. |
| distributed.eval.perDeviceBatchSize | int | `8` | Batch size to use for evaluation for each device. |
| distributed.eval.validationSplitPercentage | float | `0.2` | The percentage of the train set used as validation set in case there's no validation split. Set to 0.20 for a 20% validation split. |
| distributed.logLevel | string | `"info"` | The Hugging Face Transformers logging level (`debug`, `info`, `warning`, `error`, and `critical`). |
| distributed.modelNameOrPath | string | `"meta-llama/Llama-2-7b-chat-hf"` | The name or path of the pretrained model to pass to the Hugging Face transformers training arguments. |
| distributed.quantize.outputDir | string | `"/tmp/pvc-mount/output/quantized_model"` |  |
| distributed.quantize.peftModelDir | string | `"/tmp/pvc-mount/output/saved_model"` |  |
| distributed.quantize.woqAlgo | string | `"RTN"` |  |
| distributed.quantize.woqBits | int | `8` |  |
| distributed.quantize.woqGroupSize | int | `-1` |  |
| distributed.quantize.woqScheme | string | `"sym"` |  |
| distributed.script | string | `"/workspace/scripts/finetune.py"` | The script that will be executed using `torch.distributed.launch`. |
| distributed.train.bf16 | bool | `true` | Whether to use bf16 (mixed) precision instead of 32-bit. Requires hardware that supports bfloat16. |
| distributed.train.dataFile | string | `nil` | Path to a Llama formatted data file to use, if no dataset name is provided. |
| distributed.train.datasetConcatenation | bool | `true` | Whether to concatenate the sentence for more efficient training. |
| distributed.train.datasetName | string | `"medalpaca/medical_meadow_medical_flashcards"` | Name of a Hugging Face dataset to use. If no dataset name is provided, the dataFile path will be used instead. |
| distributed.train.ddpBackend | string | `"ccl"` | The backend to be used for distributed training. It is recommended to use `ccl` with the Intel Extension for PyTorch. |
| distributed.train.ddpFindUnusedParameters | bool | `false` | The `find_used_parameters` flag to pass to DistributedDataParallel. |
| distributed.train.epochs | int | `1` | Number of training epochs to perform. |
| distributed.train.gradientAccumulationSteps | int | `1` | Number of updates steps to accumulate before performing a backward/update pass. |
| distributed.train.inputColumnName | string | `nil` | Name of the column in the dataset that optionally provides context or input for the task. If no column name is provided, the "input" column is used. |
| distributed.train.instructionColumnName | string | `nil` | Name of the column in the dataset that describes the task that the model should perform. If no column name is provided, the "instruction" column is used. |
| distributed.train.learningRate | float | `0.00002` | The initial learning rate. |
| distributed.train.loggingSteps | int | `1` | Log every X updates steps. Should be an integer or a float in range `[0,1]`. If smaller than 1, will be interpreted as ratio of total training steps. |
| distributed.train.loraAlpha | int | `16` | Alpha parameter in the LoRA method. |
| distributed.train.loraDropout | float | `0.1` | Dropout parameter in the LoRA method. |
| distributed.train.loraRank | int | `8` | Rank parameter in the LoRA method. |
| distributed.train.loraTargetModules | string | `"q_proj vproj"` | Target modules for the LoRA method. |
| distributed.train.maxSteps | int | `-1` | If set to a positive number, the total number of training steps to perform. Overrides the number of training epochs. |
| distributed.train.noCuda | bool | `true` | Use CPU when set to true. |
| distributed.train.outputColumnName | string | `nil` | Name of the column in the dataset with the answer to the instruction. If no column name is provided, the "output" column is used. |
| distributed.train.outputDir | string | `"/tmp/pvc-mount/output/saved_model"` | The output directory where the model predictions and checkpoints will be written. |
| distributed.train.overwriteOutputDir | bool | `true` | Overwrite the content of the output directory. Use this to continue training if output_dir points to a checkpoint directory. |
| distributed.train.perDeviceBatchSize | int | `8` | The batch size per device. |
| distributed.train.promptWithInput | string | `"Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request."` | Prompt string for an instruction with context |
| distributed.train.promptWithoutInput | string | `"Below is an instruction that describes a task. Write a response that appropriately completes the request."` | Prompt string for an instruction without context |
| distributed.train.saveStrategy | string | `"epoch"` | The checkpoint save strategy to use (`no`, `steps`, or `epoch`). |
| distributed.train.saveTotalLimit | int | `2` | If a value is passed, will limit the total amount of checkpoints. Deletes the older checkpoints in `output_dir`. |
| distributed.train.useFastTokenizer | bool | `false` | Whether to use one of the fast tokenizer (backed by the tokenizers library) or not. |
| distributed.train.useIpex | bool | `true` | Use Intel #xtension for PyTorch when it is available. |
| distributed.train.useLora | bool | `true` | Whether or not to use LoRA. |
| distributed.workers | int | `4` | The number of worker pods to deploy. |
| elasticPolicy.maxReplicas | int | `4` | The upper limit for the number of pods that can be set by the autoscaler. Cannot be smaller than `elasticPolicy.minReplicas` or `distributed.workers`. |
| elasticPolicy.maxRestarts | int | `10` | The maximum number of restart times for pods in elastic mode. |
| elasticPolicy.minReplicas | int | `1` | The lower limit for the number of replicas to which the job can scale down. |
| elasticPolicy.rdzvBackend | string | `"c10d"` | The rendezvous backend type (c10d, etcd, or etcd-v2). |
| envVars.cclWorkerCount | int | `1` | Value for the CCL_WORKER_COUNT environment variable. Must be >1 to use the CCL DDP backend. |
| envVars.ftpProxy | string | `nil` | Set the ftp_proxy environment variable. |
| envVars.hfDatasetsCache | string | `"/tmp/pvc-mount/hf_dataset_cache"` | Path to a directory used to cache Hugging Face datasets using the HF_DATASETS_CACHE environment variable. |
| envVars.hfHome | string | `"/tmp/home"` | Sets the `HF_HOME` environment variable and is used as the volume mount location for your Hugging Face token. |
| envVars.httpProxy | string | `nil` | Set the http_proxy environment variable. |
| envVars.httpsProxy | string | `nil` | Set the https_proxy environment variable. |
| envVars.ldPreload | string | `"/usr/lib/x86_64-linux-gnu/libtcmalloc.so.4.5.9:/usr/local/lib/libiomp5.so"` | Paths set to the LD_PRELOAD environment variable. |
| envVars.logLevel | string | `"INFO"` | Value set to the LOG_LEVEL environment variable. |
| envVars.noProxy | string | `nil` | Set the no_proxy environment variable. |
| envVars.socksProxy | string | `nil` | Set the socks_proxy environment variable. |
| envVars.transformersCache | string | `"/tmp/pvc-mount/transformers_cache"` | Location for the Transformers cache (using the TRANSFORMERS_CACHE environment variable). |
| image.name | string | `"intel/ai-workflows"` | Name of the image to use for the PyTorch job. The container should include the fine tuning script and all the dependencies required to run the job. |
| image.pullPolicy | string | `"IfNotPresent"` | Determines when the kubelet will pull the image to the worker nodes. Choose from: `IfNotPresent`, `Always`, or `Never`. If updates to the image have been made, use `Always` to ensure the newest image is used. |
| image.tag | string | `"torch-2.3.0-huggingface-multinode-py3.10"` | The image tag for the container that will be used to run the PyTorch job. The container should include the fine tuning script and all the dependencies required to run the job. |
| resources.cpuLimit | string | `nil` | Optionally specify the maximum amount of CPU resources for each worker, where 1 CPU unit is equivalent to 1 physical CPU core or 1 virtual core. For more information see the [Kubernetes documentation on CPU resource units](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#meaning-of-cpu). |
| resources.cpuRequest | string | `nil` | Optionally specify the amount of CPU resources requested for each worker, where 1 CPU unit is equivalent to 1 physical CPU core or 1 virtual core. For more information see the [Kubernetes documentation on CPU resource units](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#meaning-of-cpu). |
| resources.memoryLimit | string | `nil` | Optionally specify the maximum amount of memory resources for each worker. For more information see the [Kubernetes documentation on memory resource units](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#meaning-of-memory). |
| resources.memoryRequest | string | `nil` | Optionally specify the amount of memory resources requested for each worker. For more information see the [Kubernetes documentation on memory resource units](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#meaning-of-memory). |
| resources.nodeSelectorLabel | string | `nil` | Optionally specify a label for the type of node that will be used for the PyTorch job workers. |
| resources.nodeSelectorValue | string | `nil` | If `resources.nodeSelectorLabel` is set, specify the value for the node selector label. |
| secret.encodedToken | string | `nil` | Hugging Face token encoded using base64. |
| securityContext.allowPrivilegeEscalation | bool | `false` | Boolean indicating if a process can gain more privileges than its parent process. |
| securityContext.fsGroup | string | `nil` | File system group ID to run as a non-root user |
| securityContext.runAsGroup | string | `nil` | Group ID to run as a non-root user |
| securityContext.runAsUser | string | `nil` | User ID to run as a non-root user |
| storage.pvcMountPath | string | `"/tmp/pvc-mount"` | The location where the persistent volume claim will be mounted in the worker pods. |
| storage.resources | string | `"50Gi"` | Specify the [capacity](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#capacity) for the persistent volume claim. |
| storage.storageClassName | string | `"nfs-client"` | Name of the storage class to use for the persistent volume claim. To list the available storage classes use: `kubectl get storageclass`. |

</details>

### Fine tuning Llama2 7b on a Kubernetes cluster

1. Get a [Hugging Face token](https://huggingface.co/docs/hub/security-tokens) with read access and use your terminal
   to get the base64 encoding for your token using a terminal using `echo <your token> | base64`.

   For example:

   ```bash
   $ echo hf_ABCDEFG | base64
   aGZfQUJDREVGRwo=
   ```

   Copy and paste the encoded token value into your values yaml file `encodedToken` field in the `secret` section.
   For example:

   ```yaml
   secret:
     name: hf-token-secret
     encodedToken: aGZfQUJDREVGRwo=
   ```

2. Edit your values file based on the parameters that you would like to use and your cluster. Key parameters to look
   at and edit are:
   * `image.name` if have built your own container, otherwise the default `intel/ai-workflows` image will be used
   * `image.tag` if have built your own container, otherwise the default `torch-2.3.0-huggingface-multinode-py3.10` tag will be used
   * `elasticPolicy.minReplicas` and `elasticPolicy.maxReplicas` based on the number of workers being used
   * `distributed.workers` should be set to the number of worker that will be used for the job
   * If you are using `values.yaml` for your own workload, fill in either `train.datasetName` (the name of a
     Hugging Face dataset to use) or `train.dataFile` (the path to a data file to use). If a data file is being used,
     we will upload the file to the volume after the helm chart has been deployed to the cluster.
   * `resources.cpuRequest` and `resources.cpuLimit` values should be updated based on the number of cpu cores available
     on your nodes in your cluster
   * `resources.memoryRequest` and `resources.memoryLimit` values should be updated based on the amount of memory
     available on the nodes in your cluster
   * `resources.nodeSelectorLabel` and `resources.nodeSelectorValue` specify a node label key/value to indicate which
     type of nodes can be used for the worker pods. `kubectl get nodes` and `kubectl describe node <node name>` can be
     used to get information about the nodes on your cluster.
   * `storage.storageClassName` should be set to your Kubernetes NFS storage class name (use `kubectl get storageclass`
     to see a list of storage classes on your cluster)

   In the same values file, edit the security context parameters to have the containers run with a non-root user:
   * `securityContext.runAsUser` should be set to your user ID (UID)
   * `securityContext.runAsGroup` should be set to your group ID
   * `securityContext.fsGroup` should be set to your file system group ID

   See a complete list and descriptions of the available parameters the
   [Helm chart values table](#helm-chart-values-table) above.

3. Deploy the helm chart to the cluster using the `kubeflow` namespace:

   ```bash
   # Navigate to the directory that contains the Hugging Face LLM fine tuning workflow
   cd workflows/charts/huggingface-llm

   # Deploy the job using the helm chart, specifying the values file with the -f parameter
   helm install --namespace kubeflow -f <values file>.yaml llama2-distributed .
   ```

4. (Optional) If a custom dataset is being used, the file needs to be uploaded to the persistent volume claim (PVC), so
   that it can be accessed by the worker pods. If your values yaml file is using a Hugging Face dataset (such as
   `medical_meadow_values.yaml` which uses `medalpaca/medical_meadow_medical_flashcards`), you can skip this step.

   The dataset can be uploaded to the PVC using the [`kubectl cp` command](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#cp).
   The destination path for the dataset needs to match the `train.dataFile` path in your values yaml file.  Note that
   the worker pods would keep failing and restarting until you upload your dataset.

   ```bash
   # Copies a local "dataset" folder to the PVC at /tmp/pvc-mount/dataset
   kubectl cp dataset <dataaccess pod name>:/tmp/pvc-mount/dataset

   # Verify that the data file is at the expected path
   kubectl exec <dataaccess pod name> -- ls -l /tmp/pvc-mount/dataset
   ```

   For example:

   The [`financial_chatbot_values.yaml`](financial_chatbot_values.yaml) file requires this step for uploading the
   custom dataset to the cluster. Run the [`download_financial_dataset.sh`](scripts/download_financial_dataset.sh)
   script to create a custom dataset and copy it to the PVC, as mentioned below.

   ```bash
   # Set a location for the dataset to download
   export DATASET_DIR=/tmp/dataset

   # Run the download shell script
   bash scripts/download_financial_dataset.sh

   # Copy the local "dataset" folder to the PVC at /tmp/pvc-mount/dataset
   kubectl cp ${DATASET_DIR} <dataaccess pod name>:/tmp/pvc-mount/dataset
   ```

5. The training job can be monitored using by checking the status of the PyTorchJob using:
   * `kubectl get pytorchjob -n kubeflow`: Lists the PyTorch jobs that have been deployed to the cluster along with
     their status.
   * `kubectl describe pytorchjob <job name> -n kubeflow`: Lists the details of a particular PyTorch job, including
     information about events related to the job, such as pods getting created for each worker.
   The worker pods can be monitored using:
   * `kubectl get pods -n kubeflow`: To see the pods in the `kubeflow` namespace and their status. Also, adding
     `-o wide` to the command will additionally list out which node each pod is running on.
   * `kubectl logs <pod name> -n kubeflow`: Dumps the log for the specified pod. Add `-f` to the command to
     stream/follow the logs as the pod is running.

6. After the job completes, files can be copied from the persistent volume claim to your local system using the
   [`kubectl cp` command](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#cp) using the
   data access pod. The path to the trained model is in the values file field called `distributed.train.outputDir` and
   if quantization was also done, the quanted model path is in the `distributed.quantize.outputDir` field.

   As an example, the trained model from the Medical Meadows use case can be copied from the
   `/tmp/pvc-mount/output/bf16` path to the local system using the following command:

   ```bash
   kubectl cp --namespace kubeflow <dataaccess pod name>:/tmp/pvc-mount/output/saved_model .
   ```

7. Finally, the resources can be deleted from the cluster using the
   [`helm uninstall`](https://helm.sh/docs/helm/helm_uninstall/) command. For example:

   ```bash
   helm uninstall --namespace kubeflow llama2-distributed
   ```

   A list of all the deployed helm releases can be seen using `helm list`.

## Citations

```text
@misc{touvron2023llama,
      title={Llama 2: Open Foundation and Fine-Tuned Chat Models},
      author={Hugo Touvron and Louis Martin and Kevin Stone and Peter Albert and Amjad Almahairi and Yasmine Babaei and Nikolay Bashlykov and Soumya Batra and Prajjwal Bhargava and Shruti Bhosale and Dan Bikel and Lukas Blecher and Cristian Canton Ferrer and Moya Chen and Guillem Cucurull and David Esiobu and Jude Fernandes and Jeremy Fu and Wenyin Fu and Brian Fuller and Cynthia Gao and Vedanuj Goswami and Naman Goyal and Anthony Hartshorn and Saghar Hosseini and Rui Hou and Hakan Inan and Marcin Kardas and Viktor Kerkez and Madian Khabsa and Isabel Kloumann and Artem Korenev and Punit Singh Koura and Marie-Anne Lachaux and Thibaut Lavril and Jenya Lee and Diana Liskovich and Yinghai Lu and Yuning Mao and Xavier Martinet and Todor Mihaylov and Pushkar Mishra and Igor Molybog and Yixin Nie and Andrew Poulton and Jeremy Reizenstein and Rashi Rungta and Kalyan Saladi and Alan Schelten and Ruan Silva and Eric Michael Smith and Ranjan Subramanian and Xiaoqing Ellen Tan and Binh Tang and Ross Taylor and Adina Williams and Jian Xiang Kuan and Puxin Xu and Zheng Yan and Iliyan Zarov and Yuchen Zhang and Angela Fan and Melanie Kambadur and Sharan Narang and Aurelien Rodriguez and Robert Stojnic and Sergey Edunov and Thomas Scialom},
      year={2023},
      eprint={2307.09288},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}

@article{han2023medalpaca,
  title={MedAlpaca--An Open-Source Collection of Medical Conversational AI Models and Training Data},
  author={Han, Tianyu and Adams, Lisa C and Papaioannou, Jens-Michalis and Grundmann, Paul and Oberhauser, Tom and L{\"o}ser, Alexander and Truhn, Daniel and Bressem, Keno K},
  journal={arXiv preprint arXiv:2304.08247},
  year={2023}
}
```
