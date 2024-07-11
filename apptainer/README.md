# Apptainer

Apptainer (formerly Singularity) is an [open-source](https://github.com/apptainer/apptainer) container platform that allows users to build and run containers in a simple, portable and secure way. It is part of the [Linux Foundation](https://apptainer.org/news/community-announcement-20211130/).

## Install Apptainer

You will need a linux system to install and use apptainers. You can install Apptainer either from source or from pre-built packages. Refer to installation instructions provided [here](https://apptainer.org/docs/admin/main/installation.html).

## Project Setup

Define your project's registry and repository each time you use the project:

```bash
export REGISTRY=<registry_name>
export REPO=<repo_name>

apptainer registry login docker://${REGISTRY}

# Verify your access permissions
apptainer pull oras://$REGISTRY/$REPO:latest-sif
```

You can refer to the [link](https://apptainer.org/docs/user/latest/docker_and_oci.html#containers-from-other-registries) for
Apptainer support for different container registries.

## Build and Push Apptainer

To build and push an apptainer container with python ingredient you can do the following:

```bash
cd apptainer/python
apptainer build apptainer.sif apptainer.def
```

To configure the container, use `--build-arg` to override default build arguments provided in the `%arguments` section of the apptainer definition file. For example:

```bash
export BASE_IMAGE_TAG=<specific OS base image tag>
export PYTHON_VERSION=<specific python version>

apptainer build --build-arg BASE_IMAGE_TAG=$BASE_IMAGE_TAG \
--build-arg PYTHON_VERSION=$PYTHON_VERSION \
apptainer-python.sif apptainer.def
apptainer push apptainer-python.sif  oras://$REGISTRY/$REPO:python-sif
```

## GitHub Actions CI/CD

The composite action performs build, push and clean up of apptainer images for a given `input_dir` directory.

Inputs for the actions:

```bash
inputs:
  group_dir:
    description: Directory to build
    required: true
    type: string
  registry:
    description: Container Registry URL
    required: true
    type: string
  repo:
    description: Container Project Repository
    required: true
    type: string
```

See an [Example](../.github/workflows/apptainer-ci.yaml#L62) implementation of the action.
