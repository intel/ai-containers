# Workflows

This directory contains workflows demonstrating showing how the Intel Optimized base containers can be used for
different use cases:

## PyTorch Workflows

| Base Container | Device Type | Example | Description |
|----------------|-------------|---------|-------------|
| `intel/intel-optimized-pytorch:2.3.0-pip-multinode` | CPU | [Distributed LLM Fine Tuning with Kubernetes](charts/training/huggingface_llm) | Demonstrates using Hugging Face Transformers with Intel® Xeon® Scalable Processors to fine tune LLMs with multiple nodes from a Kubernetes cluster. The example includes a LLM fine tuning script, Dockerfile, and Helm chart. |
