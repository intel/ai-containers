# Fine Tuning a LLM using a Kubernetes Cluster

In order to speed up the amount of time it takes to train a model using Intel® Xeon® Scalable Processors, multiple
machines can be used to distribute the workload. This guide will focus on using multiple nodes from a
[Kubernetes](https://kubernetes.io) cluster to fine tune Llama2. It uses the [meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
and [meta-llama/Llama-2-7b-hf](https://huggingface.co/meta-llama/Llama-2-7b-hf) pretrained models from
[Hugging Face Hub](https://huggingface.co), but similar large language models can be substituted into the same template.
The [PyTorch Training operator](https://www.kubeflow.org/docs/components/training/pytorch/) from
[Kubeflow](https://www.kubeflow.org) is used to deploy the distributed training job to the Kubernetes cluster. To
optimize the performance, [Intel® Extension for PyTorch](https://github.com/intel/intel-extension-for-pytorch) is used
during training and the [Intel® oneAPI Collective Communications Library (oneCCL)](https://github.com/oneapi-src/oneCCL)
is used as the DDP backend. The `intel/intel-optimized-pytorch:2.2.0-pip-multinode` base image already includes these
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

An image has been published to DockerHub (`intel/ai-workflows:torch-2.2.0-huggingface-multinode-py3.10`) with
the following major packages included:

| Package Name | Version | Purpose |
|--------------|---------|---------|
| [PyTorch](https://pytorch.org/) | 2.2.0+cpu | Base framework to train models |
| [Intel® Extension for PyTorch](https://github.com/intel/intel-extension-for-pytorch) | 2.2.0+cpu | Utilizes Intel®'s optimization |
| [Intel® Neural Compressor](https://github.com/intel/neural-compressor) | 2.4.1 | Optimize model for inference post-training |
| [Intel® oneAPI Collective Communications Library](https://github.com/oneapi-src/oneCCL) | 2.2.0+cpu | Deploy PyTorch jobs on multiple nodes |

See the [build from source instructions](../../../../tensorflow/README.md#build-from-source) to build a custom LLM fine
tuning container.

## Running the distributed training job

> Prior to running the examples, ensure that your Kubernetes cluster meets the
> [cluster requirements](#cluster-requirements) mentioned above.

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

### Fine tuning Llama2 7b on a Kubernetes cluster

> Before running the fine tuning job on the cluster, the Docker image must be built and pushed to a container
> registry or loaded into Docker on the cluster nodes. See the [container build](#container-build) and
> [container push](#container-push) sections for instructions.

1. Get a [Hugging Face token](https://huggingface.co/docs/hub/security-tokens) with read access and use your terminal
   to get the base64 encoding for your token using a terminal using `echo <your token> | base64`.

   For example:
   ```
   $ echo hf_ABCDEFG | base64
   aGZfQUJDREVGRwo=
   ```

   Copy and paste the encoded token value into your values yaml file `encodedToken` field in the `secret` section.
   For example:
   ```
   secret:
     name: hf-token-secret
     encodedToken: aGZfQUJDREVGRwo=
   ```

2. Edit your values file based on the parameters that you would like to use and your cluster. Key parameters to look
   at and edit are:
   * `image.name` if have built your own container, otherwise the default `intel/ai-workflows` image will be used
   * `image.tag` if have built your own container, otherwise the default `torch-2.2.0-huggingface-multinode-py3.10` tag will be used
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

   See a complete list and descriptions of the available parameters in the [Helm chart values documentation](values.md).

3. Deploy the helm chart to the cluster using the `kubeflow` namespace:
   ```
   # Navigate to the directory that contains the Hugging Face LLM fine tuning workflow
   cd workflows/charts/training/huggingface_llm

   # Deploy the job using the helm chart, specifying the values file with the -f parameter
   helm install --namespace kubeflow -f <values file>.yaml llama2-distributed .
   ```

4. (Optional) If a custom dataset is being used, the file needs to be uploaded to the persistent volume claim (PVC), so
   that it can be accessed by the worker pods. If your values yaml file is using a Hugging Face dataset (such as
   `medical_meadow_values.yaml` which uses `medalpaca/medical_meadow_medical_flashcards`), you can skip this step.

   The dataset can be uploaded to the PVC using the [`kubectl cp` command](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#cp).
   The destination path for the dataset needs to match the `train.dataFile` path in your values yaml file.  Note that
   the worker pods would keep failing and restarting until you upload your dataset.
   ```
   # Copies a local "dataset" folder to the PVC at /tmp/pvc-mount/dataset
   kubectl cp dataset <dataaccess pod name>:/tmp/pvc-mount/dataset

   # Verify that the data file is at the expected path
   kubectl exec <dataaccess pod name> -- ls -l /tmp/pvc-mount/dataset
   ```

   For example:

   The [`financial_chatbot_values.yaml`](financial_chatbot_values.yaml) file requires this step for uploading the
   custom dataset to the cluster. Run the [`download_financial_dataset.sh`](scripts/download_financial_dataset.sh)
   script to create a custom dataset and copy it to the PVC, as mentioned below.

   ```
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
   ```
   kubectl cp --namespace kubeflow <dataaccess pod name>:/tmp/pvc-mount/output/saved_model .
   ```
7. Finally, the resources can be deleted from the cluster using the
   [`helm uninstall`](https://helm.sh/docs/helm/helm_uninstall/) command. For example:
   ```
   helm uninstall --namespace kubeflow llama2-distributed
   ```
   A list of all the deployed helm releases can be seen using `helm list`.

## Citations

```
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
