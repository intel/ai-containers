#!/bin/bash

# Copyright (c) 2024 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

## Checks if drivers are installed correctly
device=$(clinfo | grep 'Intel(R) Data Center GPU')

if [[ $device == "" ]]; then
	echo "Intel(R) Data Center GPU not found! Drivers not found/aren't correctly installed!"
	exit 1
fi

## checks for the presence of MKL,DPCPP and CCL/MPI Packages in OneAPI directory
if [[ $RUNTIME_ONLY == "True" ]]; then
    list=(
        "/opt/intel/oneapi/redist/lib"
        "/opt/intel/oneapi/redist/lib/ccl"
        "/opt/intel/oneapi/redist/lib/mpi"
    )
elif [[ $RUNTIME_ONLY == "False" ]]; then
    list=(
        "/opt/intel/oneapi/compiler"
        "/opt/intel/oneapi/ccl"
        "/opt/intel/oneapi/dnnl"
        "/opt/intel/oneapi/mkl"
        "/opt/intel/oneapi/dpl"
    )
fi

for i in "${list[@]}"; do
	if [[ ! -d "${i}" ]]; then
		echo "OneAPI libraries not found/installed!"
		exit 1
	fi
done

echo "Intel XPU drivers and OneAPI runtime packages are correctly installed!"
