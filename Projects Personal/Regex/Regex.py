import re

# Basic example - Captures one or more digits. 
# Regex pattern => Serial: (\d+)
text = "Serial: 12345, Model: ABC-6789, Batch: X001"
pattern = r"Serial: (\d+)"  # Raw string notation (r"") is used to avoid escape issues
match = re.search(pattern, text)  # re.search finds the first match
if match:
    print(match.group(1), "\n")  # Output: 12345


# Advance example_1 - Extracting Multiple Values 
# Regex Pattern =>  Serial: (\d+), Model: (\w+-\d+), Batch: (\w+\d+)
text = "Serial: 12345, Model: ABC-6789, Batch: X001"
pattern = r"Serial: (\d+), Model: (\w+-\d+), Batch: (\w+\d+)"
match = re.search(pattern, text)
if match:
    serial, model, batch = match.groups()
    print("Serial:", serial)        # Output: 12345
    print("Model:", model)          # Output: ABC-6789
    print("Batch:", batch, "\n")    # Output: X001

# Advance example_2 - Lookahead ensures that the digits are followed by "XYZ" but does not include
product_codes = "Product: 1234XYZ, 5678ABC, 9999XYZ"    # Product codes string
pattern = r"\d+(?=XYZ)"                                 # Regex pattern: Extract numbers only if followed by "XYZ" (Lookahead)
matches = re.findall(pattern, product_codes)            # Find all matches


for match in matches:                                   # For to check all and  Print results
    print(match)    # Output: 1234 9999