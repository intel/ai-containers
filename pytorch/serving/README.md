# TorchServe
[TorchServe](https://pytorch.org/serve/) is a performant, flexible and easy to use tool for serving PyTorch models in production.

## Configuration
Setting up TorchServe for your production application may require additional steps depending on the type of model you are serving and how that model is served.

### Archive Model
The [Torchserve Model Archiver](https://github.com/pytorch/serve/blob/master/model-archiver/README.md) is a CLI tool found in the torchserve container as well as on [pypi](https://pypi.org/project/torch-model-archiver/). This process is very similar for the [TorchServe Workflow](https://github.com/pytorch/serve/tree/master/workflow-archiver).

Follow the instructions found in the link above depending on whether you are intending to archive a model or a workflow. Use the provided container rather than installing the archiver with the example command below:

```bash
curl -O https://download.pytorch.org/models/squeezenet1_1-b8a52dc0.pth
docker run --rm -it \
           -v $PWD:/home/model-server \
           intel/intel-optimized-pytorch:2.1.0-serving-cpu \
           torch-model-archiver --model-name squeezenet \
            --version 1.0 \
            --model-file model-archive/model.py \
            --serialized-file squeezenet1_1-b8a52dc0.pth \
            --handler image_classifier \
            --export-path /home/model-server
```

### Build Container
If a dependency required for model predictions is not found in the [requirements.txt](./requirements.txt) used to build torchserve, you will need to add a new container layer to the container with those dependencies.

1. Create a new dockerfile, this will serve as the basis to add your model dependencies into your torchserve service.

```dockerfile
FROM intel/intel-optimized-pytorch:2.1.0-serving-cpu as torchserve

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt 
```

2. Build and Test Torchserve with the new dependencies. The example below is for the squeezenet model.

```bash
# Ensure you are in the same directory as your Dockerfile
docker build -t torchserve:squeezenet .
# Download a pre-archived model for testing
curl -O https://torchserve.pytorch.org/mar_files/squeezenet1_1.mar
# Run torchserve with the pre-archived model
# Assuming that the above pre-archived model is in the current working directory
docker run -d --rm \
           -v $PWD:/home/model-server/model-store \ 
           --net=host \
           torchserve:squeezenet
# Verify that the container has launched successfully
IMAGE=$(docker ps -aqf "ancestor=torchserve:squeezenet")
docker logs $IMAGE
# Attempt to register the model and make an inference request
curl -X POST "http://localhost:8081/models?initial_workers=1&synchronous=true&url=squeezenet1_1.mar&model_name=squeezenet"
curl -O https://raw.githubusercontent.com/pytorch/serve/master/docs/images/kitten_small.jpg
curl -X POST http://localhost:8080/v2/models/squeezenet/infer -T kitten_small.jpg
# Stop the container
docker container stop $IMAGE
```

### Modify TorchServe Config File
As demonstrated in the above example, models must be registered before they can be used for predictions. The best way to ensure models are pre-registered with ideal settings is to modify the included [config file](./config.properties) for the torchserve server.

1. Add your model to the config file

```properties
...
cpu_launcher_enable=true
cpu_launcher_args=--use_logical_core

models={\
  "squeezenet": {\
    "1.0": {\
        "defaultVersion": true,\
        "marName": "squeezenet1_1.mar",\
        "minWorkers": 1,\
        "maxWorkers": 1,\
        "batchSize": 1,\
        "maxBatchDelay": 1\
    }\
  }\
}
```

>**Note:** Further customization options can be found in the [TorchServe Documentation](https://pytorch.org/serve/configuration.html#config-model).

2. Test Config File

```bash
# Assuming that the above pre-archived model is in the current working directory
docker run -d --rm \
           -v $PWD:/home/model-server/model-store \
           -v $PWD/config.properties:/home/model-server/config.properties \
           --net=host \
           torchserve:squeezenet
# Verify that the container has launched successfully
IMAGE=$(docker ps -aqf "ancestor=torchserve:squeezenet")
docker logs $IMAGE
# Check the models list
curl -X GET "http://localhost:8081/models"
# Stop the container
docker container stop $IMAGE
```

Expected Output: 

```json
{
  "models": [
    {
      "modelName": "squeezenet",
      "modelUrl": "squeezenet1_1.mar"
    }
  ]
}
```

### Simple MaaS on K8s
Using the provided [helm chart](../charts/inference) your model can scale to multiple nodes in Kubernetes (K8s). Once you have set your `KUBECONFIG` environment variable and can access your cluster, use the below instructions to deploy your model as a service.

1. Install [Helm](https://helm.sh/docs/intro/install/)

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 && \
chmod 700 get_helm.sh && \
./get_helm.sh
```

2. (Optional) Push TorchServe Image to a Private Registry

If you added layers to an existing torchserve container image in a [previous step](#build-container), use `docker push` to add that image to a private registry that your cluster can access.

3. Set up Model Storage

Your model archive file will no longer be accessible from your local environment, so it needs to be added to one of the following storage types supported by the chart:

  * S3 (via [Mountpoint](https://github.com/awslabs/mountpoint-s3/blob/main/doc/CONFIGURATION.md) or Cluster Configuration)
  * [PVC](https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/)
  * [NFS](https://kubernetes.io/docs/concepts/storage/volumes/#nfs)

4. Install TorchServe Chart

Using the provided [Chart README](../charts/inference/README.md) set the variables found in the table to match the expected model storage, cluster type, and model configuration for your service. The example below assumes that a PVC has been created with the squeezenet model found in the root directory of the volume.

```bash
helm install \
    --namespace=<namespace> \
    --set deploy.image=intel/intel-optimized-pytorch:2.1.0-serving-cpu \
    --set deploy.models='squeezenet=squeezenet1_1.mar' \
    --set deploy.storage.pvc.enable=true \
    --set deploy.storage.pvc.claimName=squeezenet \
    ipex-serving \
    ../charts/inference
```

5. Test Service

By default the service is a `NodePort` service, and is accessible from the ip address of any node in your cluster. Find a node ip with `kubectl get node -o wide` and attempt to communicate with service using the command below:

```bash
curl -X GET http://<your-node-ip>:30000/ping
curl -X GET http://<your-node-ip>:30001/models
```

>**Note:** If you are under a network proxy, you may need to unset your `http_proxy` and `no_proxy` to communicate with the nodes in your cluster with `curl`.

#### Next Steps
There are some additional steps that can be taken to prepare your service for your users:

- Enable [Autoscaling](https://github.com/pytorch/serve/blob/master/kubernetes/autoscale.md#autoscaler) via Prometheus
- Enable [Intel GPU](https://github.com/intel/intel-device-plugins-for-kubernetes/blob/main/cmd/gpu_plugin/README.md#install-to-nodes-with-intel-gpus-with-fractional-resources)
- Enable [Metrics](https://pytorch.org/serve/metrics.html) and [Metrics API](https://pytorch.org/serve/metrics_api.html).
- Enable [Profiling](https://github.com/pytorch/serve/blob/master/docs/performance_guide.md#profiling).
- Export an [INT8 Model for IPEX](https://github.com/pytorch/serve/blob/f7ae6f8281ac6e26404a6ae4d210535c9dc96d9a/examples/intel_extension_for_pytorch/README.md#creating-and-exporting-int8-model-for-intel-extension-for-pytorch)
- Integrate an [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) to your service to serve to a hostname rather than an ip address.
- Integrate [MLFlow](https://github.com/mlflow/mlflow-torchserve).
- Integrate an [SSL Certificate](https://pytorch.org/serve/configuration.html#enable-ssl) in your model config file to serve models securely.
