# Intel® AI Workflows

Demonstrating showing how the [AI Containers] can be used for different use cases:

## PyTorch Workflows

| Base Container | Device Type | Example | Description |
|----------------|-------------|---------|-------------|
| `intel/intel-optimized-pytorch:2.3.0-pip-multinode` | CPU | [Distributed LLM Fine Tuning with Kubernetes] | Demonstrates using Hugging Face Transformers with Intel® Xeon® Scalable Processors to fine tune LLMs with multiple nodes from a Kubernetes cluster. The example includes a LLM fine tuning script, Dockerfile, and Helm chart. |
| `intel/intel-optimized-pytorch:2.3.0-serving-cpu` | CPU | [TorchServe* with Kubernetes] | Demonstrates using TorchServe* with Intel® Xeon® Scalable Processors to serve models on multinodes nodes from a Kubernetes cluster. The example includes a Helm chart. |

## Build from Source

To build the images from source, clone the [AI Containers] repository, follow the main `README.md` file to setup your environment, and run the following command:

```bash
cd workflows/charts/huggingface-llm
docker compose build huggingface-llm
docker compose run huggingface-llm sh -c "python /workspace/scripts/finetune.py --help"
```

## License

View the [License](https://github.com/intel/ai-containers/blob/main/LICENSE) for the [AI Containers].

The images below also contain other software which may be under other licenses (such as Pytorch*, Jupyter*, Bash, etc. from the base).

It is the image user's responsibility to ensure that any use of The images below comply with any relevant licenses for all software contained within.

\* Other names and brands may be claimed as the property of others.

<!--Below are links used in these document. They are not rendered: -->

[AI Containers]: https://github.com/intel/ai-containers
[Distributed LLM Fine Tuning with Kubernetes]: https://github.com/intel/ai-containers/tree/main/workflows/charts/huggingface-llm
[TorchServe* with Kubernetes]: https://github.com/intel/ai-containers/tree/main/workflows/charts/torchserve
