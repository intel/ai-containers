#!/bin/bash

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
regex="([^\x00a-zA-Z]+[^\x00a-zA-Z0-9_-]+)\s*[:=]\s*([^\x00a-zA-Z0-9\/=_\-\s']+)"
key_val_pairs=$(echo "$matched_line" | grep -oP "$regex" | sed 's/: /=/g')

# Check if there is at least one key-value pair
if [[ -z "$key_val_pairs" ]]; then
  echo "Error: The matched line does not contain any valid key-value pairs."
  exit 1
fi

# Print the key-value pairs
echo "$key_val_pairs"
echo "$key_val_pairs" >> "$GITHUB_OUTPUT"
