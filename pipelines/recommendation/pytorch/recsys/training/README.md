# Pytorch Recsys Training - RecSys Challenge
## Description
This document contains instructions on how to run RecSys Challenge pipelines with make and docker compose.
## Project Structure 
```
├── analytics-with-python @ 1.0
├── docker-compose.yml
├── Makefile
└── README.md
```
[_Makefile_](Makefile)
```
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
```
[_docker-compose.yml_](docker-compose.yml)
```
services:
  recsys-challenge:
    build:
      args: 
        http_proxy: ${http_proxy}
        https_proxy: ${https_proxy}
        no_proxy: ${no_proxy}
      dockerfile: analytics-with-python/Dockerfile
    command: /mnt/code/run-all.sh
    container_name: hadoop-master
    environment: 
      - http_proxy=${http_proxy}
      - https_proxy=${https_proxy}
      - no_proxy=${no_proxy}
    hostname: hadoop-master
    image: ${FINAL_IMAGE_NAME}:training-python-3.7-buster
    ports: 
      - 8088:8088
      - 8888:8888
      - 8080:8080
      - 9870:9870
      - 9864:9864
      - 4040:4040
      - 18081:18081
    privileged: true
    volumes: 
      - ${OUTPUT_DIR}:${OUTPUT_DIR}
      - /${DATASET_DIR}:/mnt/data
      - ./tmp:/mnt
      - ./analytics-with-python/config:/mnt/config
      - ./analytics-with-python:/mnt/code
    working_dir: /mnt/code
```

# RecSys Challenge
End2End AI Workflow utilizing Analytics with Python. More information [here](https://github.com/intel-sandbox/applications.ai.appliedml.workflow.analyticswithpython)

## Quick Start
* Pull and configure the dependent repo submodule `git submodule update --init --recursive`.

* Install [Pipeline Repository Dependencies](https://github.com/intel-innersource/frameworks.ai.infrastructure.machine-learning-operations/blob/develop/pipelines/README.md)

* Other variables:

| Variable Name | Default | Notes |
| --- | --- | --- |
| FINAL_IMAGE_NAME | `recsys-challenge` | Final Docker image name |
| OUTPUT_DIR | `/output` | Output directory |
| DATASET_DIR | `/data/recsys2021` | RecSys Dataset Directory |
## Build and Run
Build and Run with defaults:
```
make recsys-challenge
```
## Build and Run Example
```
$ make recsys-challenge
./analytics-with-python/hadoop-folder-prep.sh .
-e 
remove path if already exists....
-e 
create folder for hadoop....
if ! docker network inspect hadoop ; then \
        docker network create --driver=bridge hadoop; \
fi
[]
[+] Building 0.9s (13/13) FINISHED                                                                                                                                                                        
 => [internal] load build definition from Dockerfile                                                                                                                                                 0.0s
 => => transferring dockerfile: 2.32kB                                                                                                                                                               0.0s
 => [internal] load .dockerignore                                                                                                                                                                    0.0s
 => => transferring context: 2B                                                                                                                                                                      0.0s
 => [internal] load metadata for docker.io/library/python:3.7-buster                                                                                                                                 0.8s
 => [auth] library/python:pull token for registry-1.docker.io                                                                                                                                        0.0s
 => [1/8] FROM docker.io/library/python:3.7-buster@sha256:2703aeb7b87e849ad2d4cdf25e1b21cf575ca1d2e1442a36f24017a481578222                                                                           0.0s
 => CACHED [2/8] RUN DEBIAN_FRONTEND=noninteractive apt-get -y update &&     DEBIAN_FRONTEND=noninteractive apt-get -y install --no-install-recommends openssh-server ssh wget vim net-tools git ht  0.0s
 => CACHED [3/8] RUN wget --no-check-certificate https://repo.huaweicloud.com/java/jdk/8u201-b09/jdk-8u201-linux-x64.tar.gz &&     tar -zxvf jdk-8u201-linux-x64.tar.gz &&     mv jdk1.8.0_201 /opt  0.0s
 => CACHED [4/8] RUN wget --no-check-certificate https://dlcdn.apache.org/hadoop/common/hadoop-3.3.3/hadoop-3.3.3.tar.gz &&     tar -zxvf hadoop-3.3.3.tar.gz &&     mv hadoop-3.3.3 /opt/hadoop-3.  0.0s
 => CACHED [5/8] RUN wget --no-check-certificate https://dlcdn.apache.org/spark/spark-3.3.0/spark-3.3.0-bin-hadoop3.tgz &&     tar -zxvf spark-3.3.0-bin-hadoop3.tgz &&     mv spark-3.3.0-bin-hado  0.0s
 => CACHED [6/8] RUN wget --no-check-certificate http://distfiles.macports.org/scala2.12/scala-2.12.12.tgz &&     tar -zxvf scala-2.12.12.tgz &&     mv scala-2.12.12 /opt/scala-2.12.12 &&     rm   0.0s
 => CACHED [7/8] RUN ssh-keygen -t rsa -f /root/.ssh/id_rsa -P '' &&     cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys &&     sed -i 's/#   Port 22/Port 12345/' /etc/ssh/ssh_config &&    0.0s
 => CACHED [8/8] RUN pip install --no-cache-dir pyarrow findspark numpy pandas transformers torch pyrecdp sklearn xgboost                                                                            0.0s
 => exporting to image                                                                                                                                                                               0.0s
 => => exporting layers                                                                                                                                                                              0.0s
 => => writing image sha256:a76c8bf585a22bfffe825988f7cf6213bc8b737895694a0f55a7661f4805ffb9                                                                                                         0.0s
 => => naming to docker.io/library/recsys-challenge:training-python-3.7-buster                                                                                                                       0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
[+] Running 1/0
 ⠿ Container hadoop-master  Recreated                                                                                                                                                                0.1s
Attaching to hadoop-master
hadoop-master  | 
hadoop-master  | prepare spark dev environment....
hadoop-master  | 
hadoop-master  | format namenode...
```
...
```
hadoop-master  | #########################
hadoop-master  | ### retweet_timestamp
hadoop-master  | #########################
hadoop-master  | Training.....
hadoop-master  | [0]    train-logloss:0.62301   valid-logloss:0.62302
hadoop-master  | [25]   train-logloss:0.24346   valid-logloss:0.24299
hadoop-master  | [50]   train-logloss:0.23107   valid-logloss:0.23059
hadoop-master  | [75]   train-logloss:0.22883   valid-logloss:0.22877
hadoop-master  | [100]  train-logloss:0.22766   valid-logloss:0.22803
hadoop-master  | [125]  train-logloss:0.22674   valid-logloss:0.22753
hadoop-master  | [150]  train-logloss:0.22602   valid-logloss:0.22720
hadoop-master  | [175]  train-logloss:0.22534   valid-logloss:0.22693
hadoop-master  | [200]  train-logloss:0.22477   valid-logloss:0.22675
hadoop-master  | [225]  train-logloss:0.22422   valid-logloss:0.22658
hadoop-master  | [249]  train-logloss:0.22381   valid-logloss:0.22648
hadoop-master  | Predicting...
hadoop-master  | took 228.5 seconds
hadoop-master  | #########################
hadoop-master  | ### retweet_with_comment_timestamp
hadoop-master  | #########################
hadoop-master  | Training.....
hadoop-master  | [0]    train-logloss:0.60022   valid-logloss:0.60020
hadoop-master  | [25]   train-logloss:0.05844   valid-logloss:0.05846
hadoop-master  | [50]   train-logloss:0.03246   valid-logloss:0.03270
hadoop-master  | [75]   train-logloss:0.03087   valid-logloss:0.03150
hadoop-master  | [100]  train-logloss:0.03037   valid-logloss:0.03133
hadoop-master  | [125]  train-logloss:0.03002   valid-logloss:0.03127
hadoop-master  | [150]  train-logloss:0.02971   valid-logloss:0.03125
hadoop-master  | [175]  train-logloss:0.02948   valid-logloss:0.03124
hadoop-master  | [200]  train-logloss:0.02923   valid-logloss:0.03123
hadoop-master  | [219]  train-logloss:0.02906   valid-logloss:0.03123
hadoop-master  | Predicting...
hadoop-master  | took 201.8 seconds
hadoop-master  | #########################
hadoop-master  | ### like_timestamp
hadoop-master  | #########################
hadoop-master  | Training.....
hadoop-master  | [0]    train-logloss:0.67215   valid-logloss:0.67171
hadoop-master  | [25]   train-logloss:0.55620   valid-logloss:0.55312
hadoop-master  | [50]   train-logloss:0.54695   valid-logloss:0.54384
hadoop-master  | [75]   train-logloss:0.54348   valid-logloss:0.54068
hadoop-master  | [100]  train-logloss:0.54142   valid-logloss:0.53901
hadoop-master  | [125]  train-logloss:0.53950   valid-logloss:0.53753
hadoop-master  | [150]  train-logloss:0.53816   valid-logloss:0.53661
hadoop-master  | [175]  train-logloss:0.53689   valid-logloss:0.53576
hadoop-master  | [200]  train-logloss:0.53588   valid-logloss:0.53516
hadoop-master  | [225]  train-logloss:0.53500   valid-logloss:0.53470
hadoop-master  | [249]  train-logloss:0.53422   valid-logloss:0.53431
hadoop-master  | Predicting...
hadoop-master  | took 230.8 seconds
hadoop-master  | reply_timestamp      AP:0.13177 RCE:17.21939
hadoop-master  | retweet_timestamp    AP:0.34489 RCE:19.32879
hadoop-master  | retweet_with_comment_timestamp AP:0.02778 RCE:8.86315
hadoop-master  | like_timestamp       AP:0.70573 RCE:20.61987
hadoop-master  | 0.1318 17.2194 0.3449 19.3288 0.0278 8.8631 0.7057 20.6199 
hadoop-master  | AVG AP:  0.3025420714922875
hadoop-master  | AVG RCE:  16.507797035487055
hadoop-master  | This notebook took 888.9 seconds
hadoop-master  | 
hadoop-master  | 
hadoop-master  | 
hadoop-master  | all training finished!
hadoop-master exited with code 0
sudo rm -rf tmp
```
