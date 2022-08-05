DATASET ?= sst2
FINAL_IMAGE_NAME ?= hugging-face-dlsa
MODEL ?= bert-large-cased
OUTPUT_DIR ?= /output
RELEASE ?= weekly
# Weekly Envs
WHL_WW ?= $$(date +%V)
WHL_YR ?= $$(date +%Y)

hugging-face-dlsa:
	@DATASET=${DATASET} \
	 FINAL_IMAGE_NAME=${FINAL_IMAGE_NAME} \
	 MODEL=${MODEL} \
	 OUTPUT_DIR=${OUTPUT_DIR} \
	 RELEASE=${RELEASE} \
	 WHL_WW=${WHL_WW} \
	 WHL_YR=${WHL_YR} \
 	 docker compose up hugging-face-dlsa-${RELEASE} --build

clean: 
	docker compose down
