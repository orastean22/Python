#----------------------------------------------------------------------------------------------------------------------
#-- Python Script File
#-- Created on 09/Sept/2024 
#-- Author: AdrianO
#-- Comment: extract from Json file all errors and count them
#-- Load the JSON data from the file
#-- Copy the JSON file in the same folder with the script and run
#----------------------------------------------------------------------------------------------------------------------

import json
from collections import defaultdict


jsonName = "SIC2192Log_tempDev3_240829_120003.json"
with open(jsonName, 'r') as file:
    data = json.load(file)

# Dictionary to store the count of each unique comment
comment_counts = defaultdict(int)

# Iterate through the JSON data and extract "Comment" values
for error in data:
    for line in error.get("ErrorLines", []):
        comment = line.get("Comment", "")
        if comment and comment != "CRC_b21":  # Exclude CRC_b21
            # Increment the count of this comment
            comment_counts[comment] += 1

# Print out the comments and their counts
for comment, count in comment_counts.items():
    if count == 1:
        print(repr(comment))
    else:
        print(f"{repr(comment)}: {count} time(s)")

