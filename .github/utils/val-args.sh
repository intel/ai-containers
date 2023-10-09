#!/bin/bash

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
# my-dir: my-value
# my_dir: my_value
# my_dir=my-value
# my_dir=my-value
# mydir = myvalue
# etc.
##
regex="([[:alnum:]_-]+)[[:space:]]*[:=][[:space:]]*([[:alnum:]_-]+)"
while [[ $matched_line =~ $regex ]]; do
  # Docs for BASH_REMATCH: https://www.gnu.org/software/bash/manual/html_node/Bash-Variables.html#index-BASH_005fREMATCH
  key="${BASH_REMATCH[1]}"
  value="${BASH_REMATCH[2]}"
  # Print the key and value to $GITHUB_OUTPUT
  echo "$key=$value" >> $GITHUB_OUTPUT
  
  # Remove the matched pair from the line
  matched_line="${matched_line#*"${BASH_REMATCH[0]}"}"
done
