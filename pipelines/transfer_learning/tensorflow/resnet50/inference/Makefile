CHECKPOINT_DIR ?= /output/colorectal
DATASET_DIR ?= /data
FINAL_IMAGE_NAME ?= vision-transfer-learning
OUTPUT_DIR ?= /output
PLATFORM ?= None
PRECISION ?= FP32
SCRIPT ?= colorectal

vision-transfer-learning:
	@CHECKPOINT_DIR=${CHECKPOINT_DIR} \
	 DATASET_DIR=${DATASET_DIR} \
	 FINAL_IMAGE_NAME=${FINAL_IMAGE_NAME} \
	 OUTPUT_DIR=${OUTPUT_DIR} \
	 PLATFORM=${PLATFORM} \
	 PRECISION=${PRECISION} \
	 SCRIPT=${SCRIPT} \
	 docker compose up vision-transfer-learning --build

clean: 
	docker compose down
