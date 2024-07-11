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

apt-get update -y
apt-get install bc -y

stock_log=$(grep "Time Consuming" <"/logs/perf-stock.log" | awk '{print $NF}')
idp_log=$(grep "Time Consuming" <"/logs/perf-$1.log" | awk '{print $NF}')

if (($(bc <<<"$idp_log < $stock_log"))); then
	echo "Success: idp_log < stock_log"
	exit 0
else
	echo "Failure: idp_log >= stock_log"
	exit 1
fi
