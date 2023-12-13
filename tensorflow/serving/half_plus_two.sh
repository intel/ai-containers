#!/bin/bash

pip install -r requirements.txt
python half_plus_two_saved_model.py
sleep 5
# REST
python half_plus_two_client.py
rm -rf half_plus_two
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
