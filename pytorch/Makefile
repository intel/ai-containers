DOCKER_BUILDKIT ?= 1
FINAL_IMAGE_NAME ?= intel-pytorch
BASE_IMAGE_NAME ?= ubuntu
BASE_OS_NAME ?= ${BASE_IMAGE_NAME}
BASE_IMAGE_TAG ?= 20.04
INC_VERSION ?= 1.12
IPEX_VERSION ?= 1.12.100
MINICONDA_VERSION ?= "py38_4.12.0-Linux-x86_64"
ONECCL_VERSION ?= 1.12.100
PACKAGE_OPTION ?= pip
PYTHON_VERSION ?= python3
PYTORCH_VERSION ?= 1.12.0+cpu
TORCHAUDIO_VERSION ?= 0.12.0
TORCHVISION_VERSION ?= 0.13.0+cpu

# Docker build and run Proxy values
DOCKER_BUILD_ARGS ?= --build-arg ftp_proxy=${ftp_proxy} --build-arg FTP_PROXY=${FTP_PROXY} --build-arg http_proxy=${http_proxy} --build-arg HTTP_PROXY=${HTTP_PROXY} --build-arg https_proxy=${https_proxy} --build-arg HTTPS_PROXY=${HTTPS_PROXY} --build-arg no_proxy=${no_proxy} --build-arg NO_PROXY=${NO_PROXY} --build-arg socks_proxy=${socks_proxy} --build-arg SOCKS_PROXY=${SOCKS_PROXY}
DOCKER_RUN_ENVS ?= --env ftp_proxy=${ftp_proxy} --env FTP_PROXY=${FTP_PROXY} --env http_proxy=${http_proxy} --env HTTP_PROXY=${HTTP_PROXY} --env https_proxy=${https_proxy} --env HTTPS_PROXY=${HTTPS_PROXY} --env no_proxy=${no_proxy} --env NO_PROXY=${NO_PROXY} --env socks_proxy=${socks_proxy} --env SOCKS_PROXY=${SOCKS_PROXY}

ipex-base:
	mkdir -p base/licensing && \
	wget -O - https://github.com/intel/intel-extension-for-pytorch/archive/v1.12.100.tar.gz | \
	tar -xz -C base/licensing --strip=2 "intel-extension-for-pytorch-1.12.100/third-party-programs/"
	@DOCKER_BUILDKIT=${DOCKER_BUILDKIT} \
	 FINAL_IMAGE_NAME=${FINAL_IMAGE_NAME} \
	 BASE_IMAGE_NAME=${BASE_IMAGE_NAME} \
	 BASE_IMAGE_TAG=${BASE_IMAGE_TAG} \
	 BASE_OS_NAME=${BASE_OS_NAME} \
	 IPEX_VERSION=${IPEX_VERSION} \
	 MINICONDA_VERSION=${MINICONDA_VERSION} \
	 PACKAGE_OPTION=${PACKAGE_OPTION} \
	 PYTHON_VERSION=${PYTHON_VERSION} \
	 PYTORCH_VERSION=${PYTORCH_VERSION} \
	 TORCHAUDIO_VERSION=${TORCHAUDIO_VERSION} \
	 TORCHVISION_VERSION=${TORCHVISION_VERSION} \
	 docker compose up --build ipex-base

openmpi: ipex-base
	@DOCKER_BUILDKIT=${DOCKER_BUILDKIT} \
	 FINAL_IMAGE_NAME=${FINAL_IMAGE_NAME} \
	 BASE_IMAGE_NAME=${BASE_IMAGE_NAME} \
	 BASE_IMAGE_TAG=${BASE_IMAGE_TAG} \
	 BASE_OS_NAME=${BASE_OS_NAME} \
	 IPEX_VERSION=${IPEX_VERSION} \
	 PACKAGE_OPTION=${PACKAGE_OPTION} \
	 docker compose up --build openmpi

mpich: ipex-base
	@DOCKER_BUILDKIT=${DOCKER_BUILDKIT} \
	 FINAL_IMAGE_NAME=${FINAL_IMAGE_NAME} \
	 BASE_IMAGE_NAME=${BASE_IMAGE_NAME} \
	 BASE_IMAGE_TAG=${BASE_IMAGE_TAG} \
	 BASE_OS_NAME=${BASE_OS_NAME} \
	 IPEX_VERSION=${IPEX_VERSION} \
	 PACKAGE_OPTION=${PACKAGE_OPTION} \
	 docker compose up --build mpich

openmpi-oneccl: openmpi
	@DOCKER_BUILDKIT=${DOCKER_BUILDKIT} \
	 FINAL_IMAGE_NAME=${FINAL_IMAGE_NAME} \
	 BASE_IMAGE_NAME=${BASE_IMAGE_NAME} \
	 BASE_IMAGE_TAG=${BASE_IMAGE_TAG} \
	 BASE_OS_NAME=${BASE_OS_NAME} \
	 IPEX_VERSION=${IPEX_VERSION} \
	 ONECCL_VERSION=${ONECCL_VERSION} \
	 PACKAGE_OPTION=${PACKAGE_OPTION} \
	 docker compose up --build openmpi-oneccl

mpich-oneccl: mpich
	@DOCKER_BUILDKIT=${DOCKER_BUILDKIT} \
	 FINAL_IMAGE_NAME=${FINAL_IMAGE_NAME} \
	 BASE_IMAGE_NAME=${BASE_IMAGE_NAME} \
	 BASE_IMAGE_TAG=${BASE_IMAGE_TAG} \
	 BASE_OS_NAME=${BASE_OS_NAME} \
	 IPEX_VERSION=${IPEX_VERSION} \
	 ONECCL_VERSION=${ONECCL_VERSION} \
	 PACKAGE_OPTION=${PACKAGE_OPTION} \
	 docker compose up --build mpich-oneccl

openmpi-oneccl-inc: openmpi-oneccl
	@DOCKER_BUILDKIT=${DOCKER_BUILDKIT} \
	 FINAL_IMAGE_NAME=${FINAL_IMAGE_NAME} \
	 BASE_IMAGE_NAME=${BASE_IMAGE_NAME} \
	 BASE_IMAGE_TAG=${BASE_IMAGE_TAG} \
	 BASE_OS_NAME=${BASE_OS_NAME} \
	 INC_VERSION=${INC_VERSION} \
	 IPEX_VERSION=${IPEX_VERSION} \
	 PACKAGE_OPTION=${PACKAGE_OPTION} \
	 PYTHON_VERSION=${PYTHON_VERSION} \
	 docker compose up --build openmpi-oneccl-inc

all: mpich-oneccl openmpi-oneccl-inc
