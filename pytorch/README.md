# PyTorch Ingredients

```mermaid
%%{init: {'theme': 'dark'}}%%
flowchart TB
  ipexbase[ipex-base]
  inc
```

## PyTorch

### Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| BASE_IMAGE_NAME | `ubuntu` | Base Operating System |
| BASE_IMAGE_TAG | `22.04` | Base Operating System Version |
| IPEX_VERSION | `2.0.0` | Intel Extension for PyTorch Version |
| MINICONDA_VERSION | `latest-Linux-x86_64` | Miniconda Version from `https://repo.anaconda.com/miniconda` |
| PACKAGE_OPTION | `pip` | Stock Python (pypi) or Intel Python (conda) (`pip` or `idp`) |
| PYTHON_VERSION | `3.10` | Python Version |
| PYTORCH_VERSION | `2.0.0+cpu` | PyTorch Version |
| TORCHAUDIO_VERSION | `2.0.1+cpu` | TorchAudio Version |
| TORCHVISION_VERSION | `0.15.1+cpu` | TorchVision Version |

### MultiNode

Built from Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| INC_VERSION | `2.1.1` | Neural Compressor Version |
| ONECCL_VERSION | `2.0.0+cpu` | TorchCCL Version |
