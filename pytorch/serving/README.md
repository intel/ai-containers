# TorchServe

[TorchServe](https://pytorch.org/serve/) is a performant, flexible and easy to use tool for serving PyTorch models in production.

## Configuration

Setting up TorchServe for your production application may require additional steps depending on the type of model you are serving and how that model is served.

### Archive Model

The [Torchserve Model Archiver](https://github.com/pytorch/serve/blob/master/model-archiver/README.md) is a command-line tool found in the torchserve container as well as on [pypi](https://pypi.org/project/torch-model-archiver/). This process is very similar for the [TorchServe Workflow](https://github.com/pytorch/serve/tree/master/workflow-archiver).

Follow the instructions found in the link above depending on whether you are intending to archive a model or a workflow. Use the provided container rather than installing the archiver with the example command below:

#### Create a Model Archive for CPU device

```bash
curl -O https://download.pytorch.org/models/squeezenet1_1-b8a52dc0.pth
docker run --rm -it \
           --entrypoint='' \
           -u root \
           -v $PWD:/home/model-server \
           intel/intel-optimized-pytorch:2.4.0-serving-cpu \
           torch-model-archiver --model-name squeezenet1_1 \
           --version 1.1 \
           --model-file model-archive/model.py \
           --serialized-file squeezenet1_1-b8a52dc0.pth \
           --handler image_classifier \
           --export-path /home/model-server
```

### Create a Model Archive for XPU device

Use a squeezenet model [optimized](./model-store/ipex_squeezenet.py) for XPU using Intel® Extension for PyTorch*.

```bash
docker run --rm -it \
           --entrypoint='' \
           -u root \
           -v $PWD:/home/model-server \
           --device /dev/dri \
           intel/intel-optimized-pytorch:2.5.10-serving-xpu \
           sh -c 'python model-archive/ipex_squeezenet.py && \
           torch-model-archiver --model-name squeezenet1_1 \
           --version 1.1 \
           --serialized-file squeezenet1_1-jit.pt \
           --handler image_classifier \
           --export-path /home/model-server'
```

### Test Model

Test Torchserve with the new archived model. The example below is for the squeezenet model.

#### Run Torchserve for CPU device

```bash
# Assuming that the above pre-archived model is in the current working directory
docker run -d --rm --name server \
          -v $PWD:/home/model-server/model-store \
          -v $PWD/wf-store:/home/model-server/wf-store \
          --net=host \
          intel/intel-optimized-pytorch:2.4.0-serving-cpu
```

#### Run Torchserve for XPU device

```bash
# Assuming that the above pre-archived model is in the current working directory
## Find the video and render groups to add to the run command

VIDEO=$(getent group video | sed -E 's,^video:[^:]*:([^:]*):.*$,\1,')
RENDER=$(getent group render | sed -E 's,^render:[^:]*:([^:]*):.*$,\1,')

docker run -d --rm --name server \
          -v $PWD:/home/model-server/model-store \
          -v $PWD/wf-store:/home/model-server/wf-store \
          -v $PWD/config-xpu.properties:/home/model-server/config.properties \
          --net=host \
          --device /dev/dri \
          --group-add ${VIDEO} \
          --group-add ${RENDER} \
          intel/intel-optimized-pytorch:2.5.10-serving-xpu
```

After lauching the container, follow the steps below:

```bash
# Verify that the container has launched successfully
docker logs server
# Attempt to register the model and make an inference request
curl -X POST "http://localhost:8081/models?initial_workers=1&synchronous=true&url=squeezenet1_1.mar&model_name=squeezenet"
curl -O https://raw.githubusercontent.com/pytorch/serve/master/docs/images/kitten_small.jpg
curl -X POST http://localhost:8080/v2/models/squeezenet/infer -T kitten_small.jpg
# Stop the container
docker container stop server
```

### Modify TorchServe Config File

As demonstrated in the above example, models must be registered before they can be used for predictions. The best way to ensure models are pre-registered with ideal settings is to modify the included [config file](./config.properties) for the torchserve server.

> [!NOTE]
> Since torchserve 0.11.1 torchserve asks for token authentication for security. We've disabled it in the config.properties by setting `disable_token_authorization=true`. If you want to enable the authentication you can find more details in the [documentation](https://github.com/pytorch/serve/blob/master/docs/token_authorization_api.md).

> [!NOTE]
> Since torchserve 0.11.1 the model API has been disabled by default. We enable the model API by setting `enable_model_api=true` in provided config.properties.

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

    > [!NOTE]
    > Further customization options can be found in the [TorchServe Documentation](https://pytorch.org/serve/configuration.html#config-model).

2. Test Config File

    ```bash
    # Assuming that the above pre-archived model is in the current working directory
    docker run -d --rm --name server \
              -v $PWD:/home/model-server/model-store \
              -v $PWD/config.properties:/home/model-server/config.properties \
              --net=host \
              intel/intel-optimized-pytorch:2.4.0-serving-cpu
    # Verify that the container has launched successfully
    docker logs server
    # Check the models list
    curl -X GET "http://localhost:8081/models"
    # Stop the container
    docker container stop server
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

### KServe

Apply Intel Optimizations to KServe by patching the serving runtimes to use Serving Containers with Intel Optimizations via `kubectl apply -f patch.yaml`

> [!NOTE]
> You can modify this `patch.yaml` file to change the serving runtime pod configuration.

#### Create an Endpoint

1. Create a volume with the follow file configuration:

    ```text
    my-volume
    ├── config
    │   └── config.properties
    └── model-store
        └── my-model.mar
    ```

2. Modify your TorchServe Server Configuration with a model snapshot like the following:

    ```text
    ...
    enable_metrics_api=true
    metrics_mode=prometheus
    model_store=/mnt/models/model-store
    model_snapshot={"name":"startup.cfg","modelCount":1,"models":{"mnist":{"1.0":{"defaultVersion":true,"marName":"mnist.mar","minWorkers":1,"maxWorkers":5,"batchSize":1,"responseTimeout":120}}}}
    ```

   > The model snapshot **MUST** contain the keys `defaultVersion`, `marName`, `minWorkers`, `maxWorkers`, `batchSize`, and `responseTimeout`. Even if your model `.mar` includes those keys.

3. Create a new endpoint

    ```yaml
    apiVersion: "serving.kserve.io/v1beta1"
    kind: "InferenceService"
    metadata:
      name: "ipex-torchserve-sample"
    spec:
      predictor:
        model:
          modelFormat:
            name: pytorch
          protocolVersion: v2
          storageUri: pvc://my-volume
    ```

4. Test the endpoint

    ```bash
    curl -v -H "Host: ${SERVICE_HOSTNAME}" http://${INGRESS_HOST}:${INGRESS_PORT}/v2/models
    ```

5. Make a Prediction
   Use this python script to convert your input to a bytes format:

   ```python
   import base64
   import json
   import argparse
   import uuid

   parser = argparse.ArgumentParser()
   parser.add_argument("filename", help="converts image to bytes array", type=str)
   args = parser.parse_args()

   image = open(args.filename, "rb")  # open binary file in read mode
   image_read = image.read()
   image_64_encode = base64.b64encode(image_read)
   bytes_array = image_64_encode.decode("utf-8")
   request = {
       "inputs": [
            {
                "name": str(uuid.uuid4()),
                "shape": [-1],
                "datatype": "BYTES",
                "data": [bytes_array],
            }
       ]
    }

    result_file = "{filename}.{ext}".format(
        filename=str(args.filename).split(".")[0], ext="json"
    )
    with open(result_file, "w") as outfile:
        json.dump(request, outfile, indent=4, sort_keys=True)
    ```

   Using the script will produce a json file to use as a prediction payload:

   ```bash
   curl -v -H "Host: ${SERVICE_HOSTNAME}" -X POST \
   http://${INGRESS_HOST}:${INGRESS_PORT}/v2/models/${MODELNAME}/infer \
   -d @./${PAYLOAD}.json
   ```

> [!TIP]
> You can find your `SERVICE_HOSTNAME` in the KubeFlow UI with the copy button and removing the `http://` from the url.

> [!TIP]
> You can find your ingress information with `kubectl get svc -n istio-system | grep istio-ingressgateway` and using the external IP and port mapped to `80`.
