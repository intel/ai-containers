# Support Matrix

=== "Framework Containers"
    === "[Python](https://hub.docker.com/r/intel/python)"
        {{ read_csv('assets/python.csv') }}
    === "[Classical ML](https://hub.docker.com/r/intel/intel-optimized-ml)"
        {{ read_csv('assets/classical-ml.csv') }}
    === "[PyTorch](https://hub.docker.com/r/intel/intel-optimized-pytorch)"
        {{ read_csv('assets/pytorch.csv') }}
    === "[TensorFlow](https://hub.docker.com/r/intel/intel-optimized-tensorflow)"
        {{ read_csv('assets/tensorflow.csv') }}

=== "Model Containers"
    === "CPU"
        === "PyTorch"
            {{ read_csv('assets/pytorch-cpu.csv') }}
        === "TensorFlow"
            {{ read_csv('assets/tensorflow-cpu.csv') }}
    === "PVC"
        === "Flex"
            {{ read_csv('assets/flex-pvc.csv') }}
        === "Max"
            {{ read_csv('assets/max-pvc.csv') }}

=== "[Preset Containers](https://github.com/intel/ai-containers/blob/main/preset/README.md)"
    === "Data Analytics"
        {{ read_csv('assets/data_analytics.csv') }}
    === "Classical ML"
        {{ read_csv('assets/classical_ml.csv') }}
    === "Deep Learning"
        {{ read_csv('assets/deep_learning.csv') }}
    === "Inference Optimization"
        {{ read_csv('assets/inference_optimization.csv') }}

=== "[Workflows](https://hub.docker.com/r/intel/ai-workflows)"
    === "[TorchServe](https://github.com/intel/ai-containers/tree/main/workflows/charts/torchserve)"
        {{ read_csv('assets/serving.csv') }}
    === "[Huggingface LLM](https://github.com/intel/ai-containers/tree/main/workflows/charts/huggingface-llm)"
        {{ read_csv('assets/genai.csv') }}
