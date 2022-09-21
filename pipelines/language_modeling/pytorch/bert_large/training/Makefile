DATASET ?= sst2
DATASET_DIR ?= /data
FINAL_IMAGE_NAME ?= hugging-face-dlsa
MODEL ?= bert-large-uncased
OUTPUT_DIR ?= /output

hugging-face-dlsa:
	mkdir ./dlsa/profiling-transformers/datasets && cp -r ${DATASET_DIR} ./dlsa/profiling-transformers/datasets
	@DATASET=${DATASET} \
	 FINAL_IMAGE_NAME=${FINAL_IMAGE_NAME} \
	 MODEL=${MODEL} \
	 OUTPUT_DIR=${OUTPUT_DIR} \
 	 docker compose up hugging-face-dlsa --build
	rm -rf ./dlsa/profiling-transformers/datasets

clean: 
	rm -rf ./dlsa/profiling-transformers/datasets
	docker compose down
