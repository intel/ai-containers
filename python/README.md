# Intel® Distribution for Python

[Intel® Distribution for Python] enhances performance and can improve your program speed from 10 to 100 times faster. It is a Python distribution that includes the [Intel® Math Kernel Library] (oneMKL) and other Intel performance libraries to enable near-native performance through acceleration of core numerical and machine learning packages.

## Images

The images below include variations for only the core packages in the [Intel® Distribution for Python] installation, or all of the packages.

| Tag(s)                 | IDP        |
| ---------------------- | ---------- |
| `3.10-full`, `latest`  | `2024.2.0` |
| `3.10-core`            | `2024.2.0` |

## Run a Performance Sample

To run a performance sample run the following commands:

```bash
git clone https://github.com/intel/ai-containers
cd ai-containers/python
docker run --rm -it \
    -v $PWD/tests:/tests \
    intel/python:latest \
    python /tests/perf_sample.py
```

### Compare the results against stock python

In the previous command, you should see a result at the bottom like: `Time Consuming: 0.03897857666015625`. We can compare this against `python:3.11-slim-bullseye`

```bash
docker run --rm -it \
    -v $PWD/tests:/tests \
    python:3.11-slim-bullseye \
    bash
pip install numpy
python /tests/perf_sample.py
```

## Build from Source (Advanced)

To build the images from source, clone the [Intel® AI Containers](https://github.com/intel/ai-containers) repository, follow the main `README.md` file to setup your environment, and run the following commands:

```bash
cd python
docker compose build idp
docker compose run idp
```

You can find the list of services below for each container in the group:

| Service Name | Description                                                         |
| ------------ | ------------------------------------------------------------------- |
| `idp`        | Base image with [Intel® Distribution for Python]                    |
| `pip`        | Equivalent python image without [Intel® Distribution for Python]    |


## License

View the [License](https://github.com/intel/ai-containers/blob/main/LICENSE) for the [Intel® Distribution for Python].

It is the image user's responsibility to ensure that any use of The images below comply with any relevant licenses for all software contained within.

\* Other names and brands may be claimed as the property of others.

<!--Below are links used in these document. They are not rendered: -->

[Intel® Distribution for Python]: https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-for-python.html#gs.9bos9m
[Intel® Math Kernel Library]: https://www.intel.com/content/www/us/en/developer/tools/oneapi/onemkl.html
