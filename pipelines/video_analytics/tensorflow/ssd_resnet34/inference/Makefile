FINAL_IMAGE_NAME ?= vdms-video-streamer
KERAS_VERSION ?= 2.10.0.dev2022062207
OUTPUT_DIR ?= /output
TF_ESTIMATOR_VERSION ?= 2.10.0.dev2022062208
TF_VERSION ?= 2.10.0.202226-cp38-cp38
VIDEO_PATH ?= $$(pwd)/mall.avi
VIDEO = $(shell basename ${VIDEO_PATH})
WHL_WW ?= 26
WHL_YR ?= 2022

vdms:
	WHL_WW=${WHL_WW} \
	WHL_YR=${WHL_YR} \
	numactl --physcpubind=51-55 --membind=1 docker compose up -d vdms

video-streamer: vdms
	FINAL_IMAGE_NAME=${FINAL_IMAGE_NAME} \
	KERAS_VERSION=${KERAS_VERSION} \
	OUTPUT_DIR=${OUTPUT_DIR} \
	TF_ESTIMATOR_VERSION=${TF_ESTIMATOR_VERSION} \
	TF_VERSION=${TF_VERSION} \
	VIDEO=${VIDEO} \
	VIDEO_PATH=${VIDEO_PATH} \
	WHL_WW=${WHL_WW} \
	WHL_YR=${WHL_YR} \
	docker compose up video-streamer --build

clean:
	docker compose down 
