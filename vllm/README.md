# Optimize LLM serving with vLLM on Intel® GPUs

vLLM is a fast and easy-to-use library for LLM inference and serving. It has evolved into a community-driven project with contributions from both academia and industry. Intel, as one of the community contributors, is working actively to bring satisfying performance with vLLM on Intel® platforms, including Intel® Xeon® Scalable Processors, Intel® discrete GPUs, as well as Intel® Gaud® AI accelerators. This blog focuses on Intel® discrete GPUs at this time and brings you the necessary information to get the workloads running well on your Intel® graphics cards.

## 1. What's Supported?

Intel GPUs benefit from enhancements brought by [vLLM V1 engine](https://blog.vllm.ai/2025/01/27/v1-alpha-release.html), including:

* Optimized Execution Loop & API Server
* Simple & Flexible Scheduler
* Zero-Overhead Prefix Caching
* Clean Architecture for Tensor-Parallel Inference
* Efficient Input Preparation
* Enhanced Support for Multimodal LLMs

Moreover, **`chunked_prefill`**, an optimization feature in vLLM that allows large prefill requests to be divided into small chunks and batched together with decode requests, is also enabled. This approach prioritizes decode requests, improving inter-token latency (ITL) and GPU utilization by combining compute-bound (prefill) and memory-bound (decode) requests in the same batch. vLLM v1 engine is built on this feature and in this release, it's also supported on intel GPUs by leveraging corresponding kernel from Intel® Extension for PyTorch\* for model execution.

In a near future release, we will support the following features.

* **Spec decode**: Speculative decoding in vLLM is a technique designed to improve inter-token latency during LLM inference by using a smaller, faster draft model to predict future tokens.
* **Sliding window**: Sliding window attention is a mechanism used in large language models to manage memory usage efficiently by limiting the context length to a fixed window size. This approach allows the model to focus on the most recent tokens while discarding older ones, which is particularly useful for handling long sequences without exceeding memory constraints.
* **FP8 KV cache**: We will support FP8 KV cache in this release with kernels from Intel® Extension for PyTorch\*. It allows for a larger number of tokens to be stored in the cache, effectively doubling the space available for KV cache allocation. This increase in storage capacity enhances throughput by enabling the processing of longer context lengths for individual requests or handling more concurrent request batches.

The table below lists models that have been verified by Intel. However, there should be broader models that are supported by vLLM work on Intel® GPUs.

| Model Type | Model |
| ---------- | ---------- |
| Text-generation | meta-llama/Llama-3.1 8B |
| Text-generation | deepseek-ai/deepseek-llm-7b-chat |
| Text-generation | mistralai/Mistral-7B-v0.1 |
| Text-generation | microsoft/Phi-3-mini-128k-instruct |
| Text-generation | Qwen/Qwen2-7B-Instruct |

## 2. Limitations

Some of vLLM V1 features may need extra support, including `torch.compile` support, LoRA, pipeline parallel on Ray, Structured outputs, EP/TP MoE, DP Attentions, prefix prefill and MLA related.

The following issues are known issues that we plan to fix in future releases:

* The `Bloke/baichuan-7B-GPTQ` model fails with `AttributeError: BaiChuanTokenizer has no attribute vocab_size` error.
* The `ranchlai/chatglm3-6B-gptq-4bit` model fails with `ChatGLMForConditionalGeneration has no vLLM implementation and the Transformers implementation is not compatible with vLLM` error.
* Sum of `input token length` and `output token length` has to be small than the `--max_position_embeddings` argument of a model to avoid error `ValueError: This model's maximum context length is xxxx tokens. However, you requested xxxx tokens (xxxx in the messages, xxxx in the completion). Please reduce the length of the messages or completion.`
* The `jakiAJK_DeepSeek-R1-Distill-Qwen-7B_GPTQ-int4` model and `Qwen_Qwen2-7B-Instruct-GPTQ-Int4` model get the `lm-eval` accuracy value to be 0.
* The `run-lm-eval-gsm-vllm-baseline.sh` script in the docker image mentioned in this blog doesn't support accuracy testing.
* When you use the docker image mentioned in this blog, you may see warning messages like `Pin memory is not supported on XPU`. These messages were mistakenly printed and can be omitted.
* `awq` models occupy memory larger than the model size. For `casperhansen/llama-3-8b-instruct-awq` model (sized 5.74 GB), 8.6GB memory was occupied.

## 3. How to Get Started

### 3.1. Prerequisite

| OS | Hardware |
| ---------- | ---------- |
| Ubuntu 24.10 | Intel® Arc™ B580 |
| Ubuntu 22.04 | Intel® Data Center GPU Max Series |

### 3.2. Prepare a Serving Environment

1. Follow [instructions](https://dgpu-docs.intel.com/driver/overview.html) to install driver packages.
2. Get the released docker image with command `docker pull intel/vllm:xpu`
3. Instantiate a docker container with command `docker run -t -d --shm-size 10g --net=host --ipc=host --privileged -v /dev/dri/by-path:/dev/dri/by-path --name=vllm-test --device /dev/dri:/dev/dri --entrypoint= intel/vllm:xpu /bin/bash`
4. Run command `docker exec -it vllm-test bash` in 2 separate terminals to enter container environments for the server and the client respectively.

\* Starting from here, all commands are expected to be run inside the docker container, if not explicitly noted.

In both environments, you may then wish to set a `HUGGING_FACE_HUB_TOKEN` environment variable to make sure necessary files can be downloaded from the HuggingFace website.

```bash
export HUGGING_FACE_HUB_TOKEN=xxxxxx
```

### 3.3. Launch Workloads

#### 3.3.1. Launch Server in the Server Environment

Command:

```bash
VLLM_USE_V1=1 W_LONG_MAX_MODEL_LEN=1 VLLM_WORKER_MULTIPROC_METHOD=spawn  python3 -m vllm.entrypoints.openai.api_server --model TechxGenus/Meta-Llama-3-8B-GPTQ --dtype=float16 --device=xpu --enforce-eager --port 8000  --block-size 32 --gpu-memory-util 0.85 --trust-remote-code --disable-sliding-window
```

Expected output:

```bash
INFO 02-20 03:20:29 api_server.py:937] Starting vLLM API server on http://0.0.0.0:8000
INFO 02-20 03:20:29 launcher.py:23] Available routes are:
INFO 02-20 03:20:29 launcher.py:31] Route: /openapi.json, Methods: HEAD, GET
INFO 02-20 03:20:29 launcher.py:31] Route: /docs, Methods: HEAD, GET
INFO 02-20 03:20:29 launcher.py:31] Route: /docs/oauth2-redirect, Methods: HEAD, GET
INFO 02-20 03:20:29 launcher.py:31] Route: /redoc, Methods: HEAD, GET
INFO 02-20 03:20:29 launcher.py:31] Route: /health, Methods: GET
INFO 02-20 03:20:29 launcher.py:31] Route: /ping, Methods: POST, GET
INFO 02-20 03:20:29 launcher.py:31] Route: /tokenize, Methods: POST
INFO 02-20 03:20:29 launcher.py:31] Route: /detokenize, Methods: POST
INFO 02-20 03:20:29 launcher.py:31] Route: /v1/models, Methods: GET
INFO 02-20 03:20:29 launcher.py:31] Route: /version, Methods: GET
INFO 02-20 03:20:29 launcher.py:31] Route: /v1/chat/completions, Methods: POST
INFO 02-20 03:20:29 launcher.py:31] Route: /v1/completions, Methods: POST
INFO 02-20 03:20:29 launcher.py:31] Route: /v1/embeddings, Methods: POST
INFO 02-20 03:20:29 launcher.py:31] Route: /pooling, Methods: POST
INFO 02-20 03:20:29 launcher.py:31] Route: /score, Methods: POST
INFO 02-20 03:20:29 launcher.py:31] Route: /v1/score, Methods: POST
INFO 02-20 03:20:29 launcher.py:31] Route: /v1/audio/transcriptions, Methods: POST
INFO 02-20 03:20:29 launcher.py:31] Route: /rerank, Methods: POST
INFO 02-20 03:20:29 launcher.py:31] Route: /v1/rerank, Methods: POST
INFO 02-20 03:20:29 launcher.py:31] Route: /v2/rerank, Methods: POST
INFO 02-20 03:20:29 launcher.py:31] Route: /invocations, Methods: POST
INFO:     Started server process [1636943]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

It may take some time. Showing `INFO:     Application startup complete.` indicates that the server is ready.

#### 3.3.2. Raise Requests for Benchmarking in the Client Environment

We leverage a [benchmarking script](https://github.com/vllm-project/vllm/blob/main/benchmarks/benchmark_serving.py) which is provided in vLLM to perform performance benchmarking. You can use your own client scripts as well.

Use the command below to shoot serving requests:

```bash
python3 benchmarks/benchmark_serving.py --model TechxGenus/Meta-Llama-3-8B-GPTQ --dataset-name random --random-input-len=1024 --random-output-len=1024 --ignore-eos --num-prompt 1 --max-concurrency 16 --request-rate inf --backend vllm --port=8000 --host 0.0.0.0
```

The command uses model `TechxGenus/Meta-Llama-3-8B-GPTQ`. Both input and output token sizes are set to `1024`. Maximally `16` requests are processed concurrently in the server.

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
