# TorchServe

[TorchServe](https://pytorch.org/serve/) is a performant, flexible and easy to use tool for serving PyTorch models in production.

## Configuration

Setting up TorchServe for your production application may require additional steps depending on the type of model you are serving and how that model is served.

### Archive Model

The [Torchserve Model Archiver](https://github.com/pytorch/serve/blob/master/model-archiver/README.md) is a command-line tool found in the torchserve container as well as on [pypi](https://pypi.org/project/torch-model-archiver/). This process is very similar for the [TorchServe Workflow](https://github.com/pytorch/serve/tree/master/workflow-archiver).

Follow the instructions found in the link above depending on whether you are intending to archive a model or a workflow. Use the provided container rather than installing the archiver with the example command below:

```bash
curl -O https://download.pytorch.org/models/squeezenet1_1-b8a52dc0.pth
docker run --rm -it \
           -v $PWD:/home/model-server \
           intel/intel-optimized-pytorch:2.2.0-serving-cpu \
           torch-model-archiver --model-name squeezenet \
            --version 1.0 \
            --model-file model-archive/model.py \
            --serialized-file squeezenet1_1-b8a52dc0.pth \
            --handler image_classifier \
            --export-path /home/model-server
```

### Test Model

Test Torchserve with the new archived model. The example below is for the squeezenet model.

```bash
# Assuming that the above pre-archived model is in the current working directory
docker run -d --rm --name server \
          -v $PWD:/home/model-server/model-store \
          --net=host \
          intel/intel-optimized-pytorch:2.2.0-serving-cpu
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
              intel/intel-optimized-pytorch:2.2.0-serving-cpu
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
