FINAL_IMAGE_NAME ?= vdms-video-streamer
OUTPUT_DIR ?= /output
VIDEO_PATH ?= $$(pwd)/classroom.mp4
MODEL_DIR ?= $$(pwd)/models
VIDEO = $(shell basename ${VIDEO_PATH})

vdms:
	numactl --physcpubind=51-55 --membind=1 docker compose up -d vdms

video-streamer: vdms
	mkdir -p ./video-streamer/models && cp -r ${MODEL_DIR}/* ./video-streamer/models
	FINAL_IMAGE_NAME=${FINAL_IMAGE_NAME} \
	OUTPUT_DIR=${OUTPUT_DIR} \
	VIDEO=${VIDEO} \
	VIDEO_PATH=${VIDEO_PATH} \
	docker compose up video-streamer --build

clean:
	docker compose down 
	rm -rf ./video-streamer/models ${VIDEO}
