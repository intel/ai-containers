BASE_IMAGE_NAME ?= ubuntu
BASE_IMAGE_TAG ?= 22.04
DOCKER_BUILDKIT ?= 1
FINAL_IMAGE_NAME ?= "classical-ml"
MINICONDA_VERSION ?= "py39_4.12.0-Linux-x86_64"
PACKAGE_OPTION ?= pip
PYTHON_VERSION ?= python3
SCIKIT_VERSION ?= "2023.0.1"
XGBOOST_VERSION ?= "1.7.4"

ml-base:
	mkdir -p base/licensing && \
	wget -O - https://github.com/intel/scikit-learn-intelex/archive/refs/tags/${SCIKIT_VERSION}.tar.gz | \
	tar -xz -C base/licensing --strip=2 "scikit-learn-intelex-${SCIKIT_VERSION}/doc/third-party-programs-sklearnex.txt" \
	"scikit-learn-intelex-${SCIKIT_VERSION}/doc/daal4py/third-party-programs.txt"
	@DOCKER_BUILDKIT=${DOCKER_BUILDKIT} \
	 BASE_IMAGE_NAME=${BASE_IMAGE_NAME} \
	 BASE_IMAGE_TAG=${BASE_IMAGE_TAG} \
	 FINAL_IMAGE_NAME=${FINAL_IMAGE_NAME} \
	 MINICONDA_VERSION=${MINICONDA_VERSION} \
	 PACKAGE_OPTION=${PACKAGE_OPTION} \
	 PYTHON_VERSION=${PYTHON_VERSION} \
	 SCIKIT_VERSION=${SCIKIT_VERSION} \
	 XGBOOST_VERSION=${XGBOOST_VERSION} \
	 docker compose up --build ml-base


all: ml-base

clean:
	rm -rf base/licensing
	docker compose down
