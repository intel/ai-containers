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
regex="([[:alnum:]_-]+)[[:space:]]*[:=][[:space:]]*([[:alnum:]\/=_\-\s']+)"
echo $matched_line | grep -oP $regex | sed 's/: /=/g' >> $GITHUB_OUTPUT
