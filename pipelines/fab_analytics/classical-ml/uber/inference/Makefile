OUTPUT_DIR ?= /output
FINAL_IMAGE_NAME ?= wafer-insights

wafer-insight:
	@OUTPUT_DIR=${OUTPUT_DIR} \
	 FINAL_IMAGE_NAME=${FINAL_IMAGE_NAME} \
 	 docker compose up wafer-insight --build

clean: 
	docker compose down
