# Intel® Optimized ML

[Intel® Extension for Scikit-learn*] enhances the performance of [Scikit-learn*] by accelerating the training and inference of machine learning models on Intel® hardware.

[XGBoost*] is an optimized distributed gradient boosting library designed to be highly efficient, flexible and portable.

## Images

The images below include [Intel® Extension for Scikit-learn*] and [XGBoost*].

| Tag(s)                                            | Intel SKLearn  | Scikit-learn | XGBoost  | Dockerfile      |
| ------------------------------------------------- | -------------- | ------------ | -------- | --------------- |
| `2024.7.0-pip-base`, `latest`                     | [v2024.7.0]    | [v1.5.2]     | [v2.1.1] | [v0.4.0]        |
| `2024.6.0-pip-base`                               | [v2024.6.0]    | [v1.5.0]     | [v2.1.0] | [v0.4.0]        |
| `2024.5.0-pip-base`                               | [v2024.5.0]    | [v1.5.0]     | [v2.1.0] | [v0.4.0]        |
| `2024.3.0-pip-base`                               | [v2024.3.0]    | [v1.4.2]     | [v2.0.3] | [v0.4.0-Beta]   |
| `2024.2.0-xgboost-2.0.3-pip-base`                 | [v2024.2.0]    | [v1.4.1]     | [v2.0.3] | [v0.4.0-Beta]   |
| `scikit-learning-2024.0.0-xgboost-2.0.2-pip-base` | [v2024.0.0]    | [v1.3.2]     | [v2.0.2] | [v0.3.4]        |

The images below additionally include [Jupyter Notebook](https://jupyter.org/) server:

| Tag(s)                                               | Intel SKLearn  | Scikit-learn | XGBoost  | Dockerfile      |
| ---------------------------------------------------- | -------------- | ------------ | -------- | --------------- |
| `2024.7.0-pip-jupyter`                               | [v2024.7.0]    | [v1.5.2]     | [v2.1.1] | [v0.4.0]        |
| `2024.6.0-pip-jupyter`                               | [v2024.6.0]    | [v1.5.1]     | [v2.1.1] | [v0.4.0]        |
| `2024.5.0-pip-jupyter`                               | [v2024.5.0]    | [v1.5.0]     | [v2.1.0] | [v0.4.0]        |
| `2024.3.0-pip-jupyter`                               | [v2024.3.0]    | [v1.4.2]     | [v2.0.3] | [v0.4.0-Beta]   |
| `2024.2.0-xgboost-2.0.3-pip-jupyter`                 | [v2024.2.0]    | [v1.4.1]     | [v2.0.3] | [v0.4.0-Beta]   |
| `scikit-learning-2024.0.0-xgboost-2.0.2-pip-jupyter` | [v2024.0.0]    | [v1.3.2]     | [v2.0.2] | [v0.3.4]        |

### Run the Jupyter Container

```bash
docker run -it --rm \
    -p 8888:8888 \
    --net=host \
    -v $PWD/workspace:/workspace \
    -w /workspace \
    intel/intel-optimized-ml:2024.2.0-xgboost-2.0.3-pip-jupyter
```

After running the command above, copy the URL (something like `http://127.0.0.1:$PORT/?token=***`) into your browser to access the notebook server.

## Images with Intel® Distribution for Python*

The images below include [Intel® Distribution for Python*]:

| Tag(s)                                            | Intel SKLearn  | Scikit-learn | XGBoost  | Dockerfile      |
| ------------------------------------------------- | -------------- | ------------ | -------- | --------------- |
| `2024.7.0-idp-base`                               | [v2024.7.0]    | [v1.5.2]     | [v2.1.1] | [v0.4.0]        |
| `2024.6.0-idp-base`                               | [v2024.6.0]    | [v1.5.1]     | [v2.1.1] | [v0.4.0]        |
| `2024.5.0-idp-base`                               | [v2024.5.0]    | [v1.5.0]     | [v2.1.0] | [v0.4.0]        |
| `2024.3.0-idp-base`                               | [v2024.3.0]    | [v1.4.1]     | [v2.1.0] | [v0.4.0]        |
| `2024.2.0-xgboost-2.0.3-idp-base`                 | [v2024.2.0]    | [v1.4.1]     | [v2.0.3] | [v0.4.0-Beta]   |
| `scikit-learning-2024.0.0-xgboost-2.0.2-idp-base` | [v2024.0.0]    | [v1.3.2]     | [v2.0.2] | [v0.3.4]        |

The images below additionally include [Jupyter Notebook](https://jupyter.org/) server:

| Tag(s)                                               | Intel SKLearn  | Scikit-learn | XGBoost  | Dockerfile      |
| ---------------------------------------------------- | -------------- | ------------ | -------- | --------------- |
| `2024.7.0-idp-jupyter`                               | [v2024.7.0]    | [v1.5.2]     | [v2.1.1] | [v0.4.0]        |
| `2024.6.0-idp-jupyter`                               | [v2024.6.0]    | [v1.5.1]     | [v2.1.1] | [v0.4.0]        |
| `2024.5.0-idp-jupyter`                               | [v2024.5.0]    | [v1.5.0]     | [v2.1.0] | [v0.4.0]        |
| `2024.3.0-idp-jupyter`                               | [v2024.3.0]    | [v1.4.0]     | [v2.1.0] | [v0.4.0]        |
| `2024.2.0-xgboost-2.0.3-idp-jupyter`                 | [v2024.2.0]    | [v1.4.1]     | [v2.0.3] | [v0.4.0-Beta]   |
| `scikit-learning-2024.0.0-xgboost-2.0.2-idp-jupyter` | [v2024.0.0]    | [v1.3.2]     | [v2.0.2] | [v0.3.4]        |

## Build from Source

To build the images from source, clone the [AI Containers](https://github.com/intel/ai-containers) repository, follow the main `README.md` file to setup your environment, and run the following command:

```bash
cd classical-ml
docker compose build ml-base
docker compose run ml-base
```

You can find the list of services below for each container in the group:

| Service Name | Description                                                         |
| ------------ | ------------------------------------------------------------------- |
| `ml-base`    | Base image with [Intel® Extension for Scikit-learn*] and [XGBoost*] |
| `jupyter`    | Adds Jupyter Notebook server                                        |

## License

View the [License](https://github.com/intel/ai-containers/blob/main/LICENSE) for the [Intel® Distribution for Python].

The images below also contain other software which may be under other licenses (such as Pytorch*, Jupyter*, Bash, etc. from the base).

It is the image user's responsibility to ensure that any use of The images below comply with any relevant licenses for all software contained within.

\* Other names and brands may be claimed as the property of others.

<!--Below are links used in these document. They are not rendered: -->

[Intel® Extension for Scikit-learn*]: https://www.intel.com/content/www/us/en/developer/tools/oneapi/scikit-learn.html
[Intel® Distribution for Python]: https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-for-python.html#gs.9bos9m
[Scikit-learn*]: https://scikit-learn.org/stable/
[XGBoost*]: https://github.com/dmlc/xgboost

[v2024.7.0]: https://github.com/intel/scikit-learn-intelex/releases/tag/2024.7.0
[v2024.6.0]: https://github.com/intel/scikit-learn-intelex/releases/tag/2024.6.0
[v2024.5.0]: https://github.com/intel/scikit-learn-intelex/releases/tag/2024.5.0
[v2024.3.0]: https://github.com/intel/scikit-learn-intelex/releases/tag/2024.3.0
[v2024.2.0]: https://github.com/intel/scikit-learn-intelex/releases/tag/2024.2.0
[v2024.0.0]: https://github.com/intel/scikit-learn-intelex/releases/tag/2024.0.0

[v1.5.2]: https://github.com/scikit-learn/scikit-learn/releases/tag/1.5.2
[v1.5.1]: https://github.com/scikit-learn/scikit-learn/releases/tag/1.5.1
[v1.5.0]: https://github.com/scikit-learn/scikit-learn/releases/tag/1.5.0
[v1.4.2]: https://github.com/scikit-learn/scikit-learn/releases/tag/1.4.2
[v1.4.1]: https://github.com/scikit-learn/scikit-learn/releases/tag/1.4.1
[v1.3.2]: https://github.com/scikit-learn/scikit-learn/releases/tag/1.3.2

[v2.1.1]: https://github.com/dmlc/xgboost/releases/tag/v2.1.1
[v2.1.0]: https://github.com/dmlc/xgboost/releases/tag/v2.1.0
[v2.0.3]: https://github.com/dmlc/xgboost/releases/tag/v2.0.3
[v2.0.2]: https://github.com/dmlc/xgboost/releases/tag/v2.0.2

[v0.4.0]: https://github.com/intel/ai-containers/blob/v0.4.0/classical-ml/Dockerfile
[v0.4.0-Beta]: https://github.com/intel/ai-containers/blob/v0.4.0-Beta/classical-ml/Dockerfile
[v0.3.4]: https://github.com/intel/ai-containers/blob/v0.3.4/classical-ml/Dockerfile
