## Build and Test Classical-ML Container

### Project structure:
```
├── Makefile
├── README.md
├── base
│   ├── Dockerfile.pip
│   └── Dockerfile.idp
├── docker-compose.yaml
```

[_docker-compose.yaml_](docker-compose.yaml)
```
version: '3'
services:
  ml-base:
    image: ${FINAL_IMAGE_NAME}-${BASE_IMAGE_NAME}-${PACKAGE_OPTION}:ml-base
    pull_policy: always
    build:
      context: ./base
      args:
        http_proxy: ${http_proxy}
        https_proxy: ${https_proxy}
        no_proxy: ${no_proxy}
        BASE_IMAGE_NAME: ${BASE_IMAGE_NAME}
        BASE_IMAGE_TAG: ${BASE_IMAGE_TAG}
        MINICONDA_VERSION: ${MINICONDA_VERSION}
        PACKAGE_OPTION: ${PACKAGE_OPTION}
        PYTHON_VERSION: ${PYTHON_VERSION}
        SCIKIT_VERSION: ${SCIKIT_VERSION}
        XGBOOST_VERSION: ${XGBOOST_VERSION}
      dockerfile: Dockerfile.${PACKAGE_OPTION}
    command: >
      bash -c "python -c 'import sklearn; print(\"Scikit version:\", sklearn.__version__)'"
```

### Build and Test with Make

```
$ make ml-base        
 => [internal] load build definition from Dockerfile.idp                                                                                                                                                                                 0.0s
 => => transferring dockerfile: 2.85kB                                                                                                                                                                                                   0.0s
 => [internal] load .dockerignore                                                                                                                                                                                                        0.0s
 => => transferring context: 2B                                                                                                                                                                                                          0.0s
 => [internal] load metadata for docker.io/library/ubuntu:22.04                                                                                                                                                                          0.6s
 => [1/9] FROM docker.io/library/ubuntu:22.04@sha256:9a0bdde4188b896a372804be2384015e90e3f84906b750c1a53539b585fbbe7f                                                                                                                    0.0s
 => [internal] load build context                                                                                                                                                                                                        0.0s
 => => transferring context: 196B                                                                                                                                                                                                        0.0s
 => CACHED [2/9] RUN apt-get update -y &&     apt-get install -y     curl     wget                                                                                                                                                       0.0s
 => CACHED [3/9] RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Linux-x86_64.sh -O miniconda.sh &&     chmod +x miniconda.sh &&     ./miniconda.sh -b -p ~/conda &&     rm ./miniconda.sh &&     ln -s ~/conda ~/m  0.0s
 => CACHED [4/9] RUN source activate idp &&     conda config --add channels intel &&     conda install  -y -q xgboost==1.7.4         daal4py         scikit-learn-intelex==2023.0.1         threadpoolctl && &&     conda clean -y --al  0.0s
 => CACHED [5/9] RUN echo "source ~/conda/etc/profile.d/conda.sh" >> /root/.bash_profile &&     echo "conda activate idp" >> /root/.bash_profile                                                                                         0.0s
 => CACHED [6/9] RUN apt-get clean                                                                                                                                                                                                       0.0s
 => CACHED [7/9] RUN echo -e 'from sklearnex import patch_sklearn\nfrom sklearnex import unpatch_sklearn\npatch_sklearn()\nprint("To disable Intel(R) Extension for Scikit-learn*, you can run: unpatch_sklearn()")' >> /.patch_sklearn  0.0s
 => CACHED [8/9] ADD licensing /licensing                                                                                                                                                                                                0.0s
 => CACHED [9/9] RUN curl https://raw.githubusercontent.com/intel/scikit-learn-intelex/2023.0.1/LICENSE -o /licensing/TF_LICENSE                                                                                                         0.0s
 => exporting to image                                                                                                                                                                                                                   0.0s
 => => exporting layers                                                                                                                                                                                                                  0.0s
 => => writing image sha256:f31fa6ae776671f78f296e9df8ce0cf762b24958bbf1a4c61768613335dcff53                                                                                                                                             0.0s
 => => naming to docker.io/library/classical-ml-ubuntu-idp:ml-base                                                                                                                                                                       0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
[+] Running 1/0
 ⠿ Container classical-ml-ml-base-1  Created                                                                                                                                                                                             0.0s
Attaching to classical-ml-ml-base-1
classical-ml-ml-base-1  | bash: /root/conda/envs/idp/lib/libtinfo.so.6: no version information available (required by bash)
classical-ml-ml-base-1  | Scikit version: 1.1.1
classical-ml-ml-base-1 exited with code 0
```
