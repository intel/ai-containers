# Intel® Optimized OpenXLA\*

Transformable numerical computing at scale combined with [Intel® Extension for OpenXLA\*], which includes a PJRT plugin implementation to seamlessly runs [JAX\*] models on Intel GPUs.

## Images

The images below include [JAX\*] and [Intel® Extension for OpenXLA\*].

| Tag(s)                     | [JAX\*]   | [Intel® Extension for OpenXLA\*] | [Flax]   | Dockerfile      |
| -------------------------- | --------- | -------------------------------- | -------- | --------------- |
| `0.4.0-pip-base`, `latest` | [v0.4.26] | [v0.4.0-jax]                     | [v0.8.2] | [v0.4.1]        |

The images below additionally include [Jupyter Notebook](https://jupyter.org/) server:

| Tag(s)              | [JAX\*]   | [Intel® Extension for OpenXLA\*] | [Flax]   | Dockerfile      |
| ------------------- | --------- | ----------------- | -------- | --------------- |
| `0.4.0-pip-jupyter` | [v0.4.26] | [v0.4.0-jax]      | [v0.8.2] | [v0.4.1]        |

### Run the Jupyter Container

```bash
docker run -it --rm \
    -p 8888:8888 \
    --net=host \
    -v $PWD/workspace:/workspace \
    -w /workspace \
    intel/intel-optimized-xla:0.4.0-pip-jupyter
```

After running the command above, copy the URL (something like `http://127.0.0.1:$PORT/?token=***`) into your browser to access the notebook server.

## Images with Intel® Distribution for Python*

The images below include [Intel® Distribution for Python*]:

| Tag(s)           | [JAX\*]   | [Intel® Extension for OpenXLA\*] | [Flax]   | Dockerfile      |
| ---------------- | --------- | ----------------- | -------- | --------------- |
| `0.4.0-idp-base` | [v0.4.26] | [v0.4.0-jax]      | [v0.8.2] | [v0.4.1]        |

The images below additionally include [Jupyter Notebook](https://jupyter.org/) server:

| Tag(s)              | [JAX\*]   | [Intel® Extension for OpenXLA\*] | [Flax]   | Dockerfile      |
| ------------------- | --------- | ----------------- | -------- | --------------- |
| `0.4.0-idp-jupyter` | [v0.4.26] | [v0.4.0-jax]      | [v0.8.2] | [v0.4.1]        |

## Build from Source

To build the images from source, clone the [AI Containers](https://github.com/intel/ai-containers) repository, follow the main `README.md` file to setup your environment, and run the following command:

```bash
cd jax
docker compose build jax-base
docker compose run -it jax-base
```

You can find the list of services below for each container in the group:

| Service Name | Description                                     |
| ------------ | ----------------------------------------------- |
| `jax-base`   | Base image with [Intel® Extension for OpenXLA\*] |
| `jupyter`    | Adds Jupyter Notebook server                    |

## License

View the [License](https://github.com/intel/ai-containers/blob/main/LICENSE) for the [Intel® Distribution for Python].

The images below also contain other software which may be under other licenses (such as Pytorch*, Jupyter*, Bash, etc. from the base).

It is the image user's responsibility to ensure that any use of The images below comply with any relevant licenses for all software contained within.

\* Other names and brands may be claimed as the property of others.

<!--Below are links used in these document. They are not rendered: -->

[Intel® Distribution for Python*]: https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-for-python.html#gs.9bos9m
[Intel® Extension for OpenXLA\*]: https://github.com/intel/intel-extension-for-openxla
[JAX\*]: https://github.com/google/jax
[Flax]: https://github.com/google/flax

[v0.4.26]: https://github.com/google/jax/releases/tag/jax-v0.4.26

[v0.4.0-jax]: https://github.com/intel/intel-extension-for-openxla/releases/tag/0.4.0

[v0.8.2]: https://github.com/google/Flax/releases/tag/v0.8.2

[v0.4.1]: https://github.com/intel/ai-containers/blob/main/jax/Dockerfile
