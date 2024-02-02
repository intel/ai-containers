# Intel® Extension for Pytorch*

[Intel® Extension for PyTorch*] extends [PyTorch*] with up-to-date feature optimizations for an extra performance boost on Intel hardware.

On Intel CPUs optimizations take advantage of the following instuction sets:

* Intel® Advanced Matrix Extensions (Intel® AMX)
* Intel® Advanced Vector Extensions 512 (Intel® AVX-512)
* Vector Neural Network Instructions (VNNI)

On Intel GPUs Intel® Extension for PyTorch* provides easy GPU acceleration through the PyTorch* `xpu` device. The following Intel GPUs are supported:

* [Intel® Arc™ A-Series Graphics]
* [Intel® Data Center GPU Flex Series]
* [Intel® Data Center GPU Max Series]

Images available here extend [Ubuntu* 22.04](https://hub.docker.com/_/ubuntu) base image with [Intel® Extension for PyTorch*] built for different use cases as well as some additional software. [Dockerfile](https://github.com/intel/ai-containers/blob/main/python/Dockerfile) used to generate these images is maintained at https://github.com/intel/ai-containers.

## CPU+GPU images

These images include support for both CPU and GPU optimizations:

| Tag(s)       | Pytorch  | IPEX          | Driver | Dockerfile |
| ------------ | -------- | ------------- | ------ | ---------- |
| `2.1.10-xpu` | [v2.1.0] | [v2.1.10+xpu] | [736]  | [v0.2.3]   |

These images additionally include [Jupiter Notebook](https://jupyter.org/) server:

| Tag(s)        | Pytorch  | IPEX           | Driver | Jupiter Port | Dockerfile |
| ------------- | -------- | -------------- | ------ | ------------ | ---------- |
| `xpu-jupyter` | [v2.0.1] | [v2.0.110+xpu] | [647]  | `8888`       | [v0.1.0]   |

## CPU only images

These images are built only with CPU optimizations (GPU acceleration support was deliberately excluded):

| Tag(s)                     | Pytorch  | IPEX         | Dockerfile |
| -------------------------- | -------- | ------------ | ---------- |
| `2.1.0-pip-base`, `latest` | [v2.1.0] | [v2.1.0+cpu] | [v0.2.3]   |
| `2.0.0-pip-base`           | [v2.0.0] | [v2.0.0+cpu] | [v0.1.0]   |

These images additionally include [Jupiter Notebook](https://jupyter.org/) server:

| Tag(s)              | Pytorch  | IPEX         | Jupiter Port | Dockerfile |
| ------------------- | -------- | ------------ | ------------ | ---------- |
| `2.1.0-pip-jupyter` | [v2.1.0] | [v2.1.0+cpu] | `8888`       | [v0.2.3]   |

These images additionally include [Intel® oneAPI Collective Communications Library] (oneCCL):

| Tag(s)                | Pytorch  | IPEX         | oneCCL               | Dockerfile |
| --------------------- | -------- | ------------ | -------------------- | ---------- |
| `2.1.0-pip-mulitnode` | [v2.1.0] | [v2.1.0+cpu] | [v2.1.0][ccl-v2.1.0] | [v0.2.3]   |
| `2.0.0-pip-multinode` | [v2.0.0] | [v2.0.0+cpu] | [v2.0.0][ccl-v2.0.0] | [v0.1.0]   |

## CPU only images with Intel® Distribution for Python*

These images are built only with CPU optimizations (GPU acceleration support was deliberately excluded) and include [Intel® Distribution for Python*]:

| Tag(s)           | Pytorch  | IPEX         | Dockerfile |
| ---------------- | -------- | ------------ | ---------- |
| `2.1.0-idp-base` | [v2.1.0] | [v2.1.0+cpu] | [v0.2.3]   |
| `2.0.0-idp-base` | [v2.0.0] | [v2.0.0+cpu] | [v0.1.0]   |

These images additionally include [Jupiter Notebook](https://jupyter.org/) server:

| Tag(s)              | Pytorch  | IPEX         | Dockerfile |
| ------------------- | -------- | ------------ | ---------- |
| `2.1.0-idp-jupyter` | [v2.1.0] | [v2.1.0+cpu] | [v0.2.3]   |

These images additionally include [Intel® oneAPI Collective Communications Library] (oneCCL):

| Tag(s)                | Pytorch  | IPEX         | oneCCL               | Dockerfile |
| --------------------- | -------- | ------------ | -------------------- | ---------- |
| `2.1.0-idp-multinode` | [v2.1.0] | [v2.1.0+cpu] | [v2.1.0][ccl-v2.1.0] | [v0.2.3]   |
| `2.0.0-idp-multinode` | [v2.0.0] | [v2.0.0+cpu] | [v2.0.0][ccl-v2.0.0] | [v0.1.0]   |

## Older releases

These images include support for CPU and [Intel® Data Center GPU Flex Series]:

| Tag(s)                             | Pytorch  | IPEX           | Driver | Dockerfile |
| ---------------------------------- | -------- | -------------- | ------ | ---------- |
| `xpu-flex-2.0.110-xpu`, `xpu-flex` | [v2.0.1] | [v2.0.110+xpu] | [647]  | [v0.1.0]   |

These images include support for CPU and [Intel® Data Center GPU Max Series]:

| Tag(s)                           | Pytorch  | IPEX           | Driver | Dockerfile |
| -------------------------------- | -------- | -------------- | ------ | ---------- |
| `xpu-max-2.0.110-xpu`, `xpu-max` | [v2.0.1] | [v2.0.110+xpu] | [647]  | [v0.1.0]   |

## License

View [license](https://github.com/intel/intel-extension-for-pytorch/blob/main/LICENSE) for the [Intel® Extension for PyTorch*].

These images also contain other software which may be under other licenses (such as Pytorch*, Jupiter*, Bash, etc. from the base).

It is the image user's responsibility to ensure that any use of these images comply with any relevant licenses for all software contained within.

\* Other names and brands may be claimed as the property of others.

[Below are links used in these document. They are not rendered.]: #

[Intel® Arc™ A-Series Graphics]: https://ark.intel.com/content/www/us/en/ark/products/series/227957/intel-arc-a-series-graphics.html
[Intel® Data Center GPU Flex Series]: https://ark.intel.com/content/www/us/en/ark/products/series/230021/intel-data-center-gpu-flex-series.html
[Intel® Data Center GPU Max Series]: https://ark.intel.com/content/www/us/en/ark/products/series/232874/intel-data-center-gpu-max-series.html

[Intel® Extension for PyTorch*]: https://intel.github.io/intel-extension-for-pytorch/
[Intel® Distribution for Python*]: https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-for-python.html
[Intel® oneAPI Collective Communications Library]: https://www.intel.com/content/www/us/en/developer/tools/oneapi/oneccl.html
[PyTorch*]: https://pytorch.org/

[v0.2.3]: https://github.com/intel/ai-containers/blob/v0.2.3/pytorch/Dockerfile
[v0.1.0]: https://github.com/intel/ai-containers/blob/v0.1.0/pytorch/Dockerfile

[v2.1.10+xpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.1.10%2Bxpu
[v2.0.110+xpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.0.110%2Bxpu

[v2.1.0]: https://github.com/pytorch/pytorch/releases/tag/v2.1.0
[v2.0.1]: https://github.com/pytorch/pytorch/releases/tag/v2.0.1
[v2.0.0]: https://github.com/pytorch/pytorch/releases/tag/v2.0.0

[v2.1.0+cpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.1.0%2Bcpu
[v2.0.0+cpu]: https://github.com/intel/intel-extension-for-pytorch/releases/tag/v2.0.0%2Bcpu

[ccl-v2.1.0]: https://github.com/intel/torch-ccl/releases/tag/v2.1.0%2Bcpu
[ccl-v2.0.0]: https://github.com/intel/torch-ccl/releases/tag/v2.1.0%2Bcpu

[736]: https://dgpu-docs.intel.com/releases/stable_736_25_20231031.html
[647]: https://dgpu-docs.intel.com/releases/stable_647_21_20230714.html
