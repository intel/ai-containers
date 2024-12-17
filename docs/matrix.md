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
    === "[Classical ML](https://hub.docker.com/r/intel/classical-ml)"
        {{ read_csv('assets/classical_ml.csv') }}
    === "[Deep Learning TensorFlow* CPU](https://hub.docker.com/r/intel/deep-learning)"
        {{ read_csv('assets/deep_learning_tensorflow-cpu.csv') }}
    === "[Deep Learning TensorFlow* GPU](https://hub.docker.com/r/intel/deep-learning)"
        {{ read_csv('assets/deep_learning_tensorflow-gpu.csv') }}
    === "[Deep Learning JAX CPU](https://hub.docker.com/r/intel/deep-learning)"
        {{ read_csv('assets/deep_learning_jax_cpu.csv') }}

=== "[Workflows](https://hub.docker.com/r/intel/ai-workflows)"
    === "[TorchServe](https://github.com/intel/ai-containers/tree/main/workflows/charts/torchserve)"
        {{ read_csv('assets/serving.csv') }}
    === "[Huggingface LLM](https://github.com/intel/ai-containers/tree/main/workflows/charts/huggingface-llm)"
        {{ read_csv('assets/genai.csv') }}
