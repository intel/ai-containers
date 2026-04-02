# Optimize LLM Serving with vLLM on Intel® GPUs

vLLM is a fast and easy-to-use library for LLM inference and serving. It has grown into a community-driven project with contributions from both academia and industry. Intel, as an active community contributor, continues to improve vLLM performance and usability on Intel® platforms, including Intel® Xeon® Scalable Processors, Intel® discrete GPUs, and Intel® Gaudi® AI accelerators. This document focuses on Intel® discrete GPUs and provides the information needed to run these workloads effectively on Intel® graphics cards.

This release is the first to switch to the optimized kernel library [vllm-xpu-kernels](https://github.com/vllm-project/vllm-xpu-kernels) for Intel® GPUs. The vLLM build included in this container uses the same code base as [v0.17.0](https://github.com/vllm-project/vllm/tree/v0.17.0) and has been validated on [Intel® Arc™ Pro B-Series Graphics](https://www.intel.com/content/www/us/en/products/docs/discrete-gpus/arc/workstations/b-series/overview.html) cards. The following bill of materials was used for validation:

| Ingredients | Version |
| --- | --- |
| Host OS | Ubuntu 25.04 |
| Python | 3.12 |
| KMD Driver | 6.14.0 |
| oneAPI | 2025.3.2 with hotfix |
| PyTorch | 2.10 |
| vllm-xpu-kernels | 0.1.4 |
| oneCCL | 2021.15.7.8 |

## 1. What's Supported?

This release supports core vLLM serving capabilities on Intel® GPUs, including online FP8 quantization, multimodal models, pooling models, and multi-GPU scaling strategies. In addition to dense-model serving, it also includes experimental expert parallelism and validated support for MoE models.

| Feature | Description | Note |
| --- | --- | --- |
| FP8 Online Quantization | vLLM supports weight-only online dynamic quantization with FP8, enabling up to a 2x reduction in model memory requirements and up to a 1.6x throughput improvement with minimal accuracy impact. Models in BF16 or FP16 can be quantized dynamically to FP8 without calibration data. | See the [example](https://docs.vllm.ai/en/stable/features/quantization/fp8/?h=online+dynamic#online-dynamic-quantization). |
| Multi-Modality Support | We support most of the popular multimodal models in upstream's [list](https://docs.vllm.ai/en/stable/models/supported_models/#list-of-multimodal-language-models), such as Qwen VL series, InternVL series, whisper-large-v3, DeepSeek-OCR, and PaddleOCR-VL. | For example, `Qwen/Qwen2.5-VL-32B-Instruct` can be launched on 4 Intel® Arc™ Pro B60 Graphics cards for multimodal processing. |
| Pooling Models Support | vLLM supports pooling models such as embedding, classification, and reward models. All of these models are now supported on Intel® GPUs. | For detailed usage, refer to the [guide](https://docs.vllm.ai/en/latest/models/pooling_models.html). |
| Pipeline Parallelism | Pipeline parallelism distributes model layers across multiple GPUs, with each GPU processing a different stage of the model in sequence. | On Intel® GPUs, this is supported on a single node with `mp` as the backend. |
| Data Parallelism | vLLM supports [Data Parallelism](https://docs.vllm.ai/en/latest/serving/data_parallel_deployment.html), where model weights are replicated across separate instances or GPUs to process independent request batches. | Supports both dense and MoE models. |
| Expert Parallelism | Experimental support for [Expert Parallelism](https://docs.vllm.ai/en/stable/serving/expert_parallel_deployment), which allows experts in Mixture-of-Experts (MoE) models to be deployed across separate GPUs. | In this release, `TP+DP+EP` is supported. |

In addition, features such as [reasoning_outputs](https://docs.vllm.ai/en/latest/features/reasoning_outputs.html), [structured_outputs](https://docs.vllm.ai/en/latest/features/structured_outputs.html), and [tool calling](https://docs.vllm.ai/en/latest/features/tool_calling.html) are supported. The following experimental features are also available:

* **torch.compile**: Can be enabled for the FP16/BF16 path.
* **speculative decoding**: Supports methods `n-gram`, `EAGLE`, `EAGLE3`, `medusa` and `suffix`. For detailed usage, refer to [document](https://docs.vllm.ai/en/stable/features/speculative_decoding/).
* **async scheduling**: Can be enabled by `--async-scheduling`. This may help reduce the CPU overheads, leading to better latency and throughput.

## 2. Supported Models

Please note that the following table contains only the models verified by Intel. Support on Intel® GPUs through vLLM extends to a wider array of models.

### Text Generation Models

These models primarily accept the LLM.generate API. Chat/Instruct models additionally support the LLM.chat API.

| Model (company/model name)                | BF16/FP16 | Dynamic Online FP8 | MXFP4 |
|-------------------------------------------| --- | --- | -- |
| openai/gpt-oss-20b                        | | |✅︎|
| openai/gpt-oss-120b                       | | |✅︎|
| deepseek-ai/DeepSeek-R1-Distill-Llama-8B  |✅︎|✅︎| |
| deepseek-ai/DeepSeek-R1-Distill-Qwen-14B  |✅︎|✅︎| |
| deepseek-ai/DeepSeek-R1-Distill-Qwen-32B  |✅︎|✅︎| |
| deepseek-ai/DeepSeek-R1-Distill-Llama-70B |✅︎|✅︎| |
| Qwen/Qwen2.5-72B-Instruct                 |✅︎|✅︎| |
| Qwen/Qwen3-14B                            |✅︎|✅︎| |
| Qwen/Qwen3-32B                            |✅︎|✅︎| |
| Qwen/Qwen3-30B-A3B                        |✅︎|✅︎| |
| Qwen/Qwen3-30B-A3B-GPTQ-Int4              |✅︎|✅︎| |
| Qwen/Qwen3-coder-30B-A3B-Instruct         |✅︎|✅︎| |
| Qwen/QwQ-32B                              |✅︎|✅︎| |
| openbmb/MiniCPM-V-4                       |✅︎|✅︎| |
| deepseek-ai/DeepSeek-V2-Lite              |✅︎|✅︎| |
| meta-llama/Llama-3.1-8B-Instruct          |✅︎|✅︎| |
| THUDM/GLM-4-9B-chat                       |✅︎|✅︎| |
| THUDM/GLM-4v-9B-chat                      |✅︎|✅︎| |
| THUDM/CodeGeex4-All-9B                    |✅︎|✅︎| |
| chuhac/TeleChat2-35B                      |✅︎|✅︎| |
| 01-ai/Yi1.5-34B-Chat                      |✅︎|✅︎| |
| THUDM/CodeGeex4-All-9B                    |✅︎|✅︎| |
| deepseek-ai/DeepSeek-Coder-33B-base       |✅︎|✅︎| |
| meta-llama/Llama-2-13b-chat-hf            |✅︎|✅︎| |
| Qwen/Qwen1.5-14B-Chat                     |✅︎|✅︎| |
| Qwen/Qwen1.5-32B-Chat                     |✅︎|✅︎| |

### Multimodal Models

The modalities(text, image, video, audio) are supported depending on the model:

| Model (company/model name)                | BF16/FP16 | Dynamic Online FP8 | Text | Image | Video | Audio |
|-------------------------------------------| --- | --- | -- | -- | -- | -- |
| openai/whisper-large-v3                   |✅︎| | | | |✅︎|
| deepseek-ai/DeepSeek-OCR                  |✅︎|✅︎|✅︎|✅︎| | |
| PaddlePaddle/PaddleOCR-VL                 |✅︎|✅︎|✅︎|✅︎| | |
| Qwen/Qwen2-VL-7B-Instruct                 |✅︎|✅︎|✅︎|✅︎|✅︎| |
| Qwen/Qwen2.5-VL-72B-Instruct              |✅︎|✅︎|✅︎|✅︎|✅︎| |
| Qwen/Qwen2.5-VL-32B-Instruct              |✅︎|✅︎|✅︎|✅︎|✅︎| |
| OpenGVLab/InternVL3_5-8B                  |✅︎|✅︎|✅︎|✅︎|✅︎| |
| OpenGVLab/InternVL3_5-14B                 |✅︎|✅︎|✅︎|✅︎|✅︎| |
| OpenGVLab/InternVL3_5-38B                 |✅︎|✅︎|✅︎|✅︎|✅︎| |
| OpenGVLab/InternVL3_5-30B-A3B             |✅︎|✅︎|✅︎|✅︎|✅︎| |
| openbmb/MiniCPM-V-4                       |✅︎|✅︎|✅︎|✅︎|✅︎| |

### Pooling Models

These models primarily support the LLM.embed API. The following table lists those that are tested on XPU.

| Model Type      | Model (company/model name)                | BF16 | Dynamic Online FP8 |
|-----------------|-------------------------------------------| --- | --- |
| Embedding Model | Qwen/Qwen3-Embedding-8B                   |✅︎|✅︎|
| Reranker Model  | Qwen/Qwen3-Reranker-8B                    |✅︎|✅︎|

## 3. Limitations

Some vLLM features still require additional enablement or refinement and are not included in current release, like LoRA (Low-Rank Adaptation), pipeline parallelism on Ray, and MLA (Multi-head Latent Attention). CPU KV-cache offloading also needs further refinement due to kernel migration.

The following items are also known issues:

* Certain workloads may show lower performance than the 0.14.1 release, as this release focuses on establishing a solid functional baseline with vLLM XPU kernels and removing IPEX dependencies. Performance optimizations will continue in future releases.
* Set the `SYCL_UR_USE_LEVEL_ZERO_V2=0` environment variable to avoid unexpected OOM errors during inference.
* Set block size to `64` for better accuracy.
* For `Qwen/Qwen3-30B-A3B` in FP16/BF16, set `PYTORCH_ALLOC_CONF=expandable_segments:True` or `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` to enable expandable blocks in the cache allocator.
* W8A8 quantized models generated with `llm_compressor` are not supported yet, such as `RedHatAI/DeepSeek-R1-Distill-Qwen-32B-FP8-dynamic`.

## 4. How to Get Started

### 4.1. Prerequisite

| OS | Hardware |
| ---------- | ---------- |
| Ubuntu 25.04 | Intel® Arc™ B-Series |

### 4.2. Prepare a Serving Environment

1. Pull the released Docker image:

   ```bash
   docker pull intel/vllm:0.17.0-xpu
   ```

2. Start a container:

   ```bash
   docker run -t -d --shm-size 10g --net=host --ipc=host --privileged \
     -v /dev/dri/by-path:/dev/dri/by-path --name=vllm-test \
     --device /dev/dri:/dev/dri --entrypoint=/bin/bash intel/vllm:0.17.0-xpu
   ```

3. Open two terminals and run `docker exec -it vllm-test bash` in both of them. Use one terminal for the server and the other for the client.

From this point on, all commands are expected to be run inside the Docker container unless noted otherwise.

In both environments, you may want to set the `HUGGING_FACE_HUB_TOKEN` environment variable to ensure that required files can be downloaded from Hugging Face.

```bash
export HUGGING_FACE_HUB_TOKEN=xxxxxx
```

### 4.3. Launch Workloads

#### 4.3.1. Launch Server in the Server Environment

Command:

```bash
VLLM_WORKER_MULTIPROC_METHOD=spawn vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-32B \
  --dtype=float16 \
  --enforce-eager \
  --port 8000 \
  --block-size 64 \
  --gpu-memory-util 0.9 \
  --no-enable-prefix-caching \
  --trust-remote-code \
  --disable-sliding-window \
  --max-num-batched-tokens=8192 \
  --max-model-len 4096 \
  -tp=4 \
  --quantization fp8
```

Expected output:

```bash
INFO 03-20 03:20:29 api_server.py:937] Starting vLLM API server on http://0.0.0.0:8000
INFO 03-20 03:20:29 launcher.py:23] Available routes are:
INFO 03-20 03:20:29 launcher.py:31] Route: /openapi.json, Methods: HEAD, GET
INFO 03-20 03:20:29 launcher.py:31] Route: /docs, Methods: HEAD, GET
INFO 03-20 03:20:29 launcher.py:31] Route: /docs/oauth2-redirect, Methods: HEAD, GET
INFO 03-20 03:20:29 launcher.py:31] Route: /redoc, Methods: HEAD, GET
INFO 03-20 03:20:29 launcher.py:31] Route: /health, Methods: GET
INFO 03-20 03:20:29 launcher.py:31] Route: /ping, Methods: POST, GET
INFO 03-20 03:20:29 launcher.py:31] Route: /tokenize, Methods: POST
INFO 03-20 03:20:29 launcher.py:31] Route: /detokenize, Methods: POST
INFO 03-20 03:20:29 launcher.py:31] Route: /v1/models, Methods: GET
INFO 03-20 03:20:29 launcher.py:31] Route: /version, Methods: GET
INFO 03-20 03:20:29 launcher.py:31] Route: /v1/chat/completions, Methods: POST
INFO 03-20 03:20:29 launcher.py:31] Route: /v1/completions, Methods: POST
INFO 03-20 03:20:29 launcher.py:31] Route: /v1/embeddings, Methods: POST
INFO 03-20 03:20:29 launcher.py:31] Route: /pooling, Methods: POST
INFO 03-20 03:20:29 launcher.py:31] Route: /score, Methods: POST
INFO 03-20 03:20:29 launcher.py:31] Route: /v1/score, Methods: POST
INFO 03-20 03:20:29 launcher.py:31] Route: /v1/audio/transcriptions, Methods: POST
INFO 03-20 03:20:29 launcher.py:31] Route: /rerank, Methods: POST
INFO 03-20 03:20:29 launcher.py:31] Route: /v1/rerank, Methods: POST
INFO 03-20 03:20:29 launcher.py:31] Route: /v2/rerank, Methods: POST
INFO 03-20 03:20:29 launcher.py:31] Route: /invocations, Methods: POST
INFO:     Started server process [1636943]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Startup may take some time. When `INFO:     Application startup complete.` appears, the server is ready.

#### 4.3.2. Raise Requests for Benchmarking in the Client Environment

Use the following command to send benchmark requests:

```bash
vllm bench serve \
  --model deepseek-ai/DeepSeek-R1-Distill-Qwen-32B \
  --dataset-name random \
  --random-input-len=1024 \
  --random-output-len=1024 \
  --ignore-eos \
  --num-prompt 16 \
  --max-concurrency 16 \
  --request-rate inf \
  --backend vllm \
  --port=8000 \
  --host 0.0.0.0 \
  --ready-check-timeout-sec 1
```

This command uses the `deepseek-ai/DeepSeek-R1-Distill-Qwen-32B` model. Both the input and output token lengths are set to `1024`, and up to `16` requests are processed concurrently by the server.

Expected output:

```bash
Maximum request concurrency: 16
============ Serving Benchmark Result ============
Successful requests:                     1
Benchmark duration (s):                  xxx
Total input tokens:                      1024
Total generated tokens:                  1024
Request throughput (req/s):              xxx
Output token throughput (tok/s):         xxx
Total Token throughput (tok/s):          xxx
---------------Time to First Token----------------
Mean TTFT (ms):                          xxx
Median TTFT (ms):                        xxx
P99 TTFT (ms):                           xxx
-----Time per Output Token (excl. 1st token)------
Mean TPOT (ms):                          xxx
Median TPOT (ms):                        xxx
P99 TPOT (ms):                           xxx
---------------Inter-token Latency----------------
Mean ITL (ms):                           xxx
Median ITL (ms):                         xxx
P99 ITL (ms):                            xxx
==================================================
```

## 5. Need Assistance?

Should you encounter any issues or have any questions, please submit an issue ticket at [vLLM Github Issues](https://github.com/vllm-project/vllm/issues). Include the text `[Intel GPU]` in the issue title to ensure it gets noticed.
