# End2End Pipelines

## Description
On this page you will find details and instructions on how to set up an environment that supports this repo's end2end pipeline container build and test infrastructure.

## Dependency Requirements
Only Linux systems are currently supported. Please make sure the following are installed in your package manager of choice:
- `make`
- `docker.io`

A full installation of [docker engine](https://docs.docker.com/engine/install/) with docker CLI is required. The recommended docker engine version is `19.03.0+`.

- `docker-compose`

The Docker Compose CLI can be [installed](https://docs.docker.com/compose/install/compose-plugin/#installing-compose-on-linux-systems) both manually and via package manager.

```
$ DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
$ mkdir -p $DOCKER_CONFIG/cli-plugins
$ curl -SL https://github.com/docker/compose/releases/download/v2.7.0/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
$ chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose

$ docker compose version
Docker Compose version v2.7.0
```

## Development Container
Rather than installing the dependencies above, a development container with the relevant dependencies for execution of MLOps validation is available for use.
### Pull from CAAS
```docker pull amr-registry.caas.intel.com/aiops/compose-devel```

### Docker Build
When building make sure to use [Intel Proxies](https://wiki.ith.intel.com/display/proxy/List+of+DMZ+Proxy+Servers+and+Ports)

```docker build -f ../.github/utils/Dockerfile.compose .```

## Build and Run Pipelines
Each pipeline will contain specific requirements and instructions for how to provide its specific dependencies and what customization options are possible. Generally, pipelines are run with the following format:

```git submodule update --init --recursive```

This will pull the dependent repo containing the scripts to run the end2end pipeline's inference and/or training.

```<KEY>=<VALUE> ... <KEY>=<VALUE> make <PIPELINE_NAME>```

Where `KEY` and `VALUE` pairs are environment variables that can be used to customize both the pipeline's script options and the resulting container.

### Cleanup
Each pipeline can remove all resources allocated by executing `make clean`.
