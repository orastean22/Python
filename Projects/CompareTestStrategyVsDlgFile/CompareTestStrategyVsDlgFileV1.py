#----------------------------------------------------------------------------------------------------------------------
#-- Python Script File
#-- Created on 04/Sept/2024
#-- Author: AdrianO
#-- Version 0.1
#-- Comment: Compare Test Strategy file Vs DLG file and display the test that are not perform in DLG but mandatory
# in Test Strategy.
# -- pip install pandas
#---------------------------------------------------------------------------------------------------------------------

import pandas as pd
import re
import warnings

# Suppress the FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)

# Load CSV file and extract test numbers and descriptions, skipping the first 18 rows
def load_csv_test_numbers(csv_file):
    # Load CSV into a DataFrame, skip the first 18 rows (to get to the actual test data)
    df = pd.read_csv(csv_file, skiprows=18)

    # Ensure columns D (index 3), E (index 4), and "Test Name" (index 5) are treated as strings
    df.iloc[:, 3] = df.iloc[:, 3].apply(lambda x: str(x))
    df.iloc[:, 4] = df.iloc[:, 4].apply(lambda x: str(x))
    df.iloc[:, 5] = df.iloc[:, 5].astype(str)

    # Format test numbers from columns D (index 3) and E (index 4)
    # Add leading zeros to ensure 3-digit format for numbers less than 100
    df.iloc[:, 3] = df.iloc[:, 3].apply(lambda x: f'{int(x):03d}' if x.isdigit() else x)
    df.iloc[:, 4] = df.iloc[:, 4].apply(lambda x: f'{int(x):03d}' if x.isdigit() else x)

    # Combine columns D and E to form test numbers (e.g., '010 010')
    df['Test_Number'] = (df.iloc[:, 3] + ' ' + df.iloc[:, 4]).str.strip()

    # Return a DataFrame containing both the test numbers and test descriptions
    return df[['Test_Number', df.columns[5]]]

# Load DLG file and extract test numbers, skipping the first 31 lines and only reading until the first ';'
def load_dlg_test_numbers(dlg_file):
    with open(dlg_file, 'r') as file:
        # Skip the first 31 lines and read the rest
        dlg_lines = file.readlines()[31:]

    test_numbers_dlg = []
    # Extract test numbers before the first ';' in each line
    for line in dlg_lines:
        if ';' in line:
            # Split at the first ';' and strip any extra whitespace
            test_num = line.split(';')[0].strip()
            # Ensure the test number is formatted like 'NNN NNN'
            if re.match(r'\d{3} \d{3}', test_num):
                test_numbers_dlg.append(test_num)

    return test_numbers_dlg

# Compare CSV test numbers with DLG test numbers
def compare_tests(csv_tests, dlg_tests):
    # Find tests that are in the CSV but not in the DLG
    missing_tests = csv_tests[~csv_tests['Test_Number'].isin(dlg_tests)]

    return missing_tests

# Main function to execute the comparison
def main():
    # Define the paths to your files
    csv_file = '2SP0215F2Q1C-GD1000HFA120C6S_TestLimits.CSV'
    dlg_file = '2024 Sept.dlg'

    # Load test numbers and descriptions from CSV and DLG files
    csv_tests = load_csv_test_numbers(csv_file)
    dlg_tests = load_dlg_test_numbers(dlg_file)

    # Compare the tests
    missing_tests = compare_tests(csv_tests, dlg_tests)

    # Display the results
    if not missing_tests.empty:
        print("The following tests from the CSV file are missing in the DLG log file:")
        for index, row in missing_tests.iterrows():
            # Display the test number and description
            print(f'{row["Test_Number"]} - {row[csv_tests.columns[1]]}')
    else:
        print("All tests from the CSV file are present in the DLG log file.")

if __name__ == '__main__':
    main()




