#!/bin/bash

source activate tensorflow-xpu

SCRIPT_DIR="$(dirname $0)"
horovodrun --verbose -np 2 --log-level=DEBUG -H localhost:2 -p 12345 python $SCRIPT_DIR/tensorflow2_keras_mnist.py
