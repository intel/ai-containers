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

set -euf -o pipefail

# Input string
input_string="$1"

# Use regex to find the line that contains '/test-group' and capture it
if [[ $input_string =~ /test-group(.*) ]]; then
	matched_line="${BASH_REMATCH[1]}"
else
	# If the pattern is not found, exit
	echo "Error: The input string does not contain a line with '/test-group'."
	exit 1
fi

# Use regex to extract key-value pairs with the cases:
# The regex now ensures that there is at least one 'a-zA-Z' value present
regex="([a-zA-Z]+[a-zA-Z0-9_-]+)\s*[:=]\s*([a-zA-Z0-9\/=_\-\s']+)"
key_val_pairs=$(echo "$matched_line" | grep -oP "$regex" | sed 's/: /=/g')

# Check if there is at least one key-value pair
if [[ -z "$key_val_pairs" ]]; then
	echo "Error: The matched line does not contain any valid key-value pairs."
	exit 1
fi

# Print the key-value pairs
echo "$key_val_pairs"
echo "$key_val_pairs" >>"$GITHUB_OUTPUT"
