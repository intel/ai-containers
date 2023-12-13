# Classical ML Ingredients

## Classical ML

### Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| BASE_IMAGE_NAME | `ubuntu` | Base Operating System |
| BASE_IMAGE_TAG | `22.04` | Base Operating System Version |
| IDP_VERSION | `core` | Intel Distribution of Python version(either `full` or `core`) |
| MINICONDA_VERSION | `latest-Linux-x86_64` | Miniconda Version from `https://repo.anaconda.com/miniconda` |
| PACKAGE_OPTION | `pip` | Stock Python (pypi) or Intel Python (conda) (`pip` or `idp`) |
| PYTHON_VERSION | `3.10` | Python Version |
| SCIKIT_VERSION | `2024.0.0` | Intel SKLearn Version |
| XGBOOST_VERSION | `2.0.2` | XGBoost Version |

### Jupyter

Built from Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| PORT | `8888` | Server UI Port |

### MLFlow

Built from Base

| Environment Variable Name | Default Value | Description |
| --- | --- | --- |
| PORT | `5000` | Server UI Port |
