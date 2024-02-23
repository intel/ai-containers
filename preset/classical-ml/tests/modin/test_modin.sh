#! /bin/bash

set -xe
mkdir -p /home/dev/data
SCRIPT_DIR=$(dirname "$0")
python "${SCRIPT_DIR}/modin_quickstart.py"
