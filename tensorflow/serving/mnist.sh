#!/bin/bash

pip install -r requirements.txt
python mnist_saved_model.py mnist
sleep 5
# grpc
python mnist_client.py --num_tests=1000 --server=localhost:8500
rm -rf mnist/
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
