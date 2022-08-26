DATASET_DIR ?= /data/recsys2021
FINAL_IMAGE_NAME ?= recsys-challenge
OUTPUT_DIR ?= /output

recsys-challenge:
	./analytics-with-python/hadoop-folder-prep.sh .
	if ! docker network inspect hadoop ; then \
		docker network create --driver=bridge hadoop; \
	fi
	@DATASET_DIR=${DATASET_DIR} \
	 FINAL_IMAGE_NAME=${FINAL_IMAGE_NAME} \
	 OUTPUT_DIR=${OUTPUT_DIR} \
 	 docker compose up recsys-challenge --build

clean: 
	sudo rm -rf tmp
	docker network rm hadoop
	DATASET_DIR=${DATASET_DIR} CONFIG_DIR=${CONFIG_DIR} docker compose down
