<ARG1> ?= <default_1>
<ARG2> ?= <default_2>
<ARG3> ?= <default_3>
FINAL_IMAGE_NAME ?= <PIPELINE_NAME>
OUTPUT_DIR ?= /output

<PIPELINE_NAME>:
	@<ARG1>=${<ARG1>} \
	 <ARG2>=${<ARG2>} \
	 <ARG3>=${<ARG3>} \
	 FINAL_IMAGE_NAME=${FINAL_IMAGE_NAME} \
	 OUTPUT_DIR=${OUTPUT_DIR} \
 	 docker compose up <PIPELINE_NAME> --build

clean: 
	docker compose down
