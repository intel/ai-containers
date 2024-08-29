# AI Containers

[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/8270/badge)](https://www.bestpractices.dev/projects/8270)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/intel/ai-containers/badge)](https://securityscorecards.dev/viewer/?uri=github.com/intel/ai-containers)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/intel/ai-containers/main.svg)](https://results.pre-commit.ci/latest/github/intel/ai-containers/main)
[![Coverage Status](https://coveralls.io/repos/github/intel/ai-containers/badge.svg?branch=main)](https://coveralls.io/github/intel/ai-containers?branch=main)
[![CodeQL](https://github.com/intel/ai-containers/actions/workflows/github-code-scanning/codeql/badge.svg?branch=main)](https://github.com/intel/ai-containers/actions/workflows/github-code-scanning/codeql)
[![Docs](https://github.com/intel/ai-containers/actions/workflows/docs.yaml/badge.svg?branch=main)](https://github.com/intel/ai-containers/actions/workflows/docs.yaml)
[![Lint](https://github.com/intel/ai-containers/actions/workflows/lint.yaml/badge.svg?branch=main)](https://github.com/intel/ai-containers/actions/workflows/lint.yaml)
[![Test Runner CI](https://github.com/intel/ai-containers/actions/workflows/test-runner-ci.yaml/badge.svg?branch=main)](https://github.com/intel/ai-containers/actions/workflows/test-runner-ci.yaml)
[![Helm Chart CI](https://github.com/intel/ai-containers/actions/workflows/chart-ci.yaml/badge.svg?event=merge_group)](https://github.com/intel/ai-containers/actions/workflows/chart-ci.yaml)
[![Weekly Tests](https://github.com/intel/ai-containers/actions/workflows/weekly-test.yaml/badge.svg?branch=main)](https://github.com/intel/ai-containers/actions/workflows/weekly-test.yaml)

This repository contains Dockerfiles, scripts, yaml files, Helm charts, etc. used to scale out AI containers with versions of TensorFlow and PyTorch that have been optimized for Intel platforms. Scaling is done with python, Docker, kubernetes, kubeflow, cnvrg.io, Helm, and other container orchestration frameworks for use in the cloud and on-premise.

## Project Setup

Define your project's registry and repository each time you use the project:

```bash
# REGISTRY/REPO:TAG
export REGISTRY=<registry_name>
export REPO=<repo_name>

docker login $REGISTRY

# Verify your access permissions
docker pull $REGISTRY/$REPO:latest
```

The maintainers of AI Containers use Azure to store containers, but an open source container registry like [harbor](https://github.com/goharbor/harbor) is preferred.

> [!WARNING]
> You can optionally skip this step and use some placeholder values, however some container groups depend on other images and will pull from a registry that you have not defined and result in an error.

### Set Up Docker Engine

You'll need to install Docker Engine on your development system. Note that while **Docker Engine** is free to use, **Docker Desktop** may require you to purchase a license.  See the [Docker Engine Server installation instructions](https://docs.docker.com/engine/install/#server) for details.

### Set Up Docker Compose

Ensure you have Docker Compose installed on your machine. If you don't have this tool installed, consult the official [Docker Compose installation documentation](https://docs.docker.com/compose/install/linux/#install-the-plugin-manually).

```bash
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.26.1/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
docker compose version
```

> [!CAUTION]
> Docker compose `v2.25.0` is the minimum required version for some container groups.

## Build Containers

Select your framework of choice (TensorFlow*, PyTorch*, Classical ML) and run the docker compose commands:

```bash
cd <framework>
docker compose up --build
```

To configure these containers, simply append the relevant environment variable to the docker compose command based on the build arguments in the compose file. For example:

```bash
# I want to build ipex-base with Intel® Distribution for Python
cd pytorch
PACKAGE_OPTION=idp docker compose up --build ipex-base
```

> [!NOTE]
> If you didn't specify `REGISTRY` or `REPO`, you also need to add the `idp` service to the list to build the dependent python image.

## Test Containers

To test the containers, use the [Test Runner Framework](https://github.com/intel/ai-containers/tree/main/test-runner):

```bash
# I want to test ipex-base with Intel® Distribution for Python
# 1. build the container in the above section
# 2. push it to a relevant registry
PACKAGE_OPTION=idp docker compose push ipex-base
cd ..
# 3. install the test runner python requirements
pip install -r test-runner/requirements.txt
# 4. Run the test file
PACKAGE_OPTION=idp python test-runner/test_runner.py -f pytorch/tests/tests.yaml
```

> [!TIP]
> To test a container built by GitHub Actions CI/CD, find the `run number` associated with the workflow run and set the `GITHUB_RUN_NUMBER` environment variable during execution to pull the desired image.

## Deploy Containers

### Install [Helm](https://helm.sh/docs/intro/install/)

This assumes you've setup [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl) and have a `KUBECONFIG`.

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 && \
chmod 700 get_helm.sh && \
./get_helm.sh
```

### Deploy a Helm Chart

```bash
cd workflows/charts
# Select a Chart and check its README for a list of customization options and other steps required.
helm install <name> \
  --namespace=<namespace> \
  --set <key>=<value> \
  <chart-folder>
```

### Test a Helm Chart

Install [Chart Testing](https://github.com/helm/chart-testing).

```bash
pip install -r workflows/charts/dev-requirements.txt
brew install chart-testing
```

Utilize the `ct` CLI to run `helm lint`, `helm install`, and `helm test`.

```bash
ct lint-and-install --namespace=<namespace> --config .github/ct.yaml --charts workflow/charts/<chart>
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
