# TensorFlow Serving
[TFServing](https://www.tensorflow.org/tfx/guide/serving) is a flexible, high-performance serving system for machine learning models, designed for production environments.

## Configuration
Setting up TensorFlow Serving for your production application may require additional steps depending on the number of models you intend to deploy and what specific performance characteristics you want to take advantage of.

### Create Server Config File
If you want to take advantage of multiple models, model versioning, model metrics, or canary deployments. You will need a [model configuration](https://www.tensorflow.org/tfx/serving/serving_config) file.

1. Add your models to `models.config`

```config
model_config_list {
  config {
    name: 'half_plus_two'
    base_path: '/models/half_plus_two'
    model_platform: 'tensorflow'
  }
  config {
    name: 'mnist'
    base_path: '/models/mnist'
    model_platform: 'tensorflow'
  }
}
```

2. Create `models` folder

The filesystem configuration required for the TFServing server looks like the following:

```text
models
├── half_plus_two
│   └── 1
│       ├── saved_model.pb
│       └── variables
├── mnist
│   └── 1
│       ├── saved_model.pb
│       └── variables
│           ├── variables.data-00000-of-00001
│           └── variables.index
└── models.config
```


3. Test Config File

```bash
# Assuming that the models directory is in your current working directory
docker run -d --rm \
           -v $PWD/models:/models \
           --net=host \
           intel/intel-extension-for-tensorflow:serving-cpu --model_config_file=/models/models.config
# Verify that the container has launched successfully
IMAGE=$(docker ps -aqf "ancestor=intel/intel-extension-for-tensorflow:serving-cpu")
docker logs $IMAGE
# Check each model status
curl -X GET http://localhost:8501/v1/models/mnist
curl -X GET http://localhost:8501/v1/models/half_plus_two
# Test one of the models
curl -X POST http://localhost:8501/v1/models/half_plus_two:predict -d '{"instances": [1, 2, 3, 4, 5]}'
# Stop the container
docker container stop $IMAGE
```

Expected Outputs: 

```json
{
 "model_version_status": [
  {
   "version": "1",
   "state": "AVAILABLE",
   "status": {
    "error_code": "OK",
    "error_message": ""
   }
  }
 ]
}
```

```json
{
    "predictions": [2.5, 3.0, 3.5, 4.0, 4.5
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

3. Set up Model Storage

Your models folder will no longer be accessible from your local environment, so it needs to be added to one of the following storage types supported by the chart:

  * S3 (via [Mountpoint](https://github.com/awslabs/mountpoint-s3/blob/main/doc/CONFIGURATION.md) or Cluster Configuration)
  * [PVC](https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/)
  * [NFS](https://kubernetes.io/docs/concepts/storage/volumes/#nfs)

4. Install TensorFlow Serving Chart

Using the provided [Chart README](../charts/inference/README.md) set the variables found in the table to match the expected model storage, cluster type, and model configuration for your service. The example below assumes that a PVC has been created with the mnist and half_plus_two models found in the root directory of the volume along with a models.config file.

```bash
helm install \
    --namespace=<namespace> \
    --set deploy.modelConfig=/models/models.config \
    --set deploy.storage.pvc.enable=true \
    --set deploy.storage.pvc.claimName=tf-serving \
    --set hpa.enable=true \
    itex-serving \
    ../charts/inference
```

5. Test Service

By default the service is a `NodePort` service, and is accessible from the ip address of any node in your cluster. Find a node ip with `kubectl get node -o wide` and attempt to communicate with service using the command below:

```bash
curl -X GET http://<your-node-ip>:30111/v1/models/mnist
curl -X GET http://<your-node-ip>:30111/v1/models/half_plus_two
curl -X POST http://<your-node-ip>:30111/v1/models/half_plus_two:predict -d '{"instances": [1, 2, 3, 4, 5]}'
```

>**Note:** If you are under a network proxy, you may need to unset your `http_proxy` and `no_proxy` to communicate with the nodes in your cluster with `curl`.

#### Next Steps
There are some additional steps that can be taken to prepare your service for your users:

- Add [Prometheus Adapter](https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus-adapter) to your HPA.
- Create a [Custom ModelServer](https://www.tensorflow.org/tfx/serving/serving_advanced)
- Enable [Intel GPU](https://github.com/intel/intel-device-plugins-for-kubernetes/blob/main/cmd/gpu_plugin/README.md#install-to-nodes-with-intel-gpus-with-fractional-resources)
- See additional [K8s Docs](https://www.tensorflow.org/tfx/serving/serving_kubernetes)
- Set up [Monitoring](https://www.tensorflow.org/tfx/serving/serving_config#monitoring_configuration)
- Set up a [Batching Configuration](https://www.tensorflow.org/tfx/serving/serving_config#batching_configuration)
- Set up Model [Versioning](https://www.tensorflow.org/tfx/serving/serving_config#serving_multiple_versions_of_a_model) and [Canary Serving](https://www.tensorflow.org/tfx/serving/serving_config#assigning_string_labels_to_model_versions_to_simplify_canary_and_rollback).
