# Intel® AI Containers

[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/8270/badge)](https://www.bestpractices.dev/projects/8270)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/intel/ai-containers/badge)](https://securityscorecards.dev/viewer/?uri=github.com/intel/ai-containers)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fintel%2Fai-containers.svg?type=shield&issueType=license)](https://app.fossa.com/projects/git%2Bgithub.com%2Fintel%2Fai-containers?ref=badge_shield&issueType=license)
[![CodeQL](https://github.com/intel/ai-containers/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/intel/ai-containers/actions/workflows/github-code-scanning/codeql)
[![Unit Tests](https://github.com/intel/ai-containers/actions/workflows/unit-test.yaml/badge.svg?branch=main)](https://github.com/intel/ai-containers/actions/workflows/unit-test.yaml)
[![Integration Tests](https://github.com/intel/ai-containers/actions/workflows/integration-test.yaml/badge.svg?branch=main)](https://github.com/intel/ai-containers/actions/workflows/integration-test.yaml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/intel/ai-containers/main.svg)](https://results.pre-commit.ci/latest/github/intel/ai-containers/main)
[![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/tylertitsworth/48dea0fc9a908a6e5ba5c5e84123bc02/raw/coverage.json)](https://gist.github.com/tylertitsworth/48dea0fc9a908a6e5ba5c5e84123bc02)

This repository contains Dockerfiles, scripts, yaml files, Helm charts, etc. used to scale out AI containers with versions of TensorFlow and PyTorch that have been optimized for Intel platforms. Scaling is done with python, Docker, kubernetes, kubeflow, cnvrg.io, Helm, and other container orchestration frameworks for use in the cloud and on-premise.

## Project Setup

Define your project's registry and repository each time you use the project:

```bash
# REGISTRY/REPO:TAG
export REGISTRY=<registry_name>
export REPO=<repo_name>
```

> [!NOTE]
> `REGISTRY` and `REPO` are used to authenticate with the private registry necessary to push completed container layers and saved them for testing and publication. For example: `REGISTRY=intel && REPO=intel-extension-for-pytorch` would become `intel/intel-extension-for-pytorch` as the name of the container image, followed by the tag generated from the service found in that project's compose file.

### Set Up Docker Engine

You'll need to install Docker Engine on your development system. Note that while **Docker Engine** is free to use, **Docker Desktop** may require you to purchase a license.  See the [Docker Engine Server installation instructions](https://docs.docker.com/engine/install/#server) for details.

### Set Up Docker Compose

Ensure you have Docker Compose installed on your machine. If you don't have this tool installed, consult the official [Docker Compose installation documentation](https://docs.docker.com/compose/install/linux/#install-the-plugin-manually).

```bash
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.25.0/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
docker compose version
```

> [!CAUTION]
> Docker compose `v2.25.0` is the minimum required version for some container groups.

## Build Ingredient Containers

Select your framework and run the docker compose commands:

```bash
cd <framework>
docker compose up --build
```

To configure ingredient containers differently, see the framework README for a table of options for each ingredient.

## Recipe Integration

To include a new recipe start by creating a new stage in a given framework's `Dockerfile`.

```dockerfile
FROM base_target AS my_recipe_target

RUN pip install -r requirements.txt
RUN ...
```

Create as many stages you want, but make sure to note your final target name. Then add a new service in the framework's `docker-compose.yaml` file.

```yaml
service_name:
  image: ${REGISTRY}/${REPO}:b-${GITHUB_RUN_NUMBER:-0}-${BASE_IMAGE_NAME:-ubuntu}-${BASE_IMAGE_TAG:-22.04}-${PACKAGE_OPTION:-pip}-py${PYTHON_VERSION:-3.10}-ipex-${IPEX_VERSION:-1.12.1}-my-package-${MY_PACKAGE_VERSION:-<version>}
  build:
    args:
      MY_PACKAGE_VERSION: ${MY_PACKAGE_VERSION:-<version>}
    target: my_recipe_target
  command: >
    sh -c "python -c 'import my_package; print(\"My Package Version:\", my_package.__version__)'"
  extends:
    service: base_target
```

For more information on how to customize your recipe, see the [docker compose documentation](https://docs.docker.com/compose/compose-file/compose-file-v3/).

### Partial Layer Integration

When re-using the AI Ingredient Containers for Intel Architectures it is often more efficient to only use portions of the image rather than all of the layers. The provided examples copy only the python environment and command-line tools installed in the image.

For Stock Python:

```dockerfile
COPY --from=intel/intel-optimized-tensorflow:<my_pip_tag> /usr/local/lib/python${PYTHON_VERSION}/dist-packages /usr/local/lib/python${PYTHON_VERSION}/dist-packages
COPY --from=intel/intel-optimized-tensorflow:<my_pip_tag> /usr/local/bin /usr/local/bin
```

For Intel Distribution for Python:

```dockerfile
COPY --from=intel/intel-optimized-tensorflow:<my_idp_tag> /root/conda/envs/idp /root/conda/envs/<my_env>
```

### Alter Existing Recipe

When changing a recipe, alter the framework's `Dockerfile` and then utilize [GitHub Actions](https://docs.github.com/en/actions/learn-github-actions) to build and test a framework. When changing a version, alter the framework's `docker-compose.yaml` file by modifying all instances of the version:

```text
${INC_VERSION:-2.1.0} -> ${INC_VERSION:-2.1.1}
```

And then build and test using GitHub Actions.

## Notebooks and MLFlow

### Jupyter

When using a container intended to launch a jupyter notebook server, start the Jupyter Server via the docker run command and copy the URL (something like `http://127.0.0.1:$PORT/?token=***`) into your browser, the port is 8888 by default.

```bash
cd <framework>
docker compose build jupyter
docker compose run -d --net=host --rm <image-name> jupyter notebook --notebook-dir=/jupyter --ip 0.0.0.0 --no-browser --allow-root
```

## Troubleshooting

- See the [Docker Troubleshooting Article](https://docs.docker.com/engine/install/troubleshoot/).
- Verify that [Docker Engine Post-Install Steps](https://docs.docker.com/engine/install/linux-postinstall/) are completed.
- When facing socket error check the group membership of the user and ensure they are part of the `docker` group.
- After changing any docker files or configs, restart the docker service `sudo systemctl restart docker`.
- Enable [Docker Desktop for WSL 2](https://docs.docker.com/desktop/windows/wsl/).
- If you are trying to access a container UI from the browser, make sure you have [port forwarded](https://code.visualstudio.com/docs/remote/ssh#_forwarding-a-port-creating-ssh-tunnel) and reconnect.
- If your environment requires a proxy to access the internet, export your development system's proxy settings to the docker environment:

```bash
export DOCKER_BUILD_ARGS="--build-arg ftp_proxy=${ftp_proxy} \
  --build-arg FTP_PROXY=${FTP_PROXY} --build-arg http_proxy=${http_proxy} \
  --build-arg HTTP_PROXY=${HTTP_PROXY} --build-arg https_proxy=${https_proxy} \
  --build-arg HTTPS_PROXY=${HTTPS_PROXY} --build-arg no_proxy=${no_proxy} \
  --build-arg NO_PROXY=${NO_PROXY} --build-arg socks_proxy=${socks_proxy} \
  --build-arg SOCKS_PROXY=${SOCKS_PROXY}"
```

```bash
export DOCKER_RUN_ENVS="-e ftp_proxy=${ftp_proxy} \
  -e FTP_PROXY=${FTP_PROXY} -e http_proxy=${http_proxy} \
  -e HTTP_PROXY=${HTTP_PROXY} -e https_proxy=${https_proxy} \
  -e HTTPS_PROXY=${HTTPS_PROXY} -e no_proxy=${no_proxy} \
  -e NO_PROXY=${NO_PROXY} -e socks_proxy=${socks_proxy} \
  -e SOCKS_PROXY=${SOCKS_PROXY}"
```

```bash
docker build $DOCKER_BUILD_ARGS -t my:tag .
docker run $DOCKER_RUN_ENVS --rm -it my:tag
```

## Support

The Intel AI MLOps team tracks bugs and enhancement requests using
[GitHub issues](https://github.com/intel/ai-containers/issues). Before submitting a
suggestion or bug report, search the existing GitHub issues to see if your issue has already been reported.

---

- [Trademarks](http://www.intel.com/content/www/us/en/legal/trademarks.html)
