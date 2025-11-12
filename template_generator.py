#!/usr/bin/env python3
"""
Template File Generator from CSV
Replaces variables in a template file based on CSV column values.
Each CSV row generates a new output file.
Uses only Python standard library - no external dependencies required.
"""

import csv
import sys
import os
import re
from pathlib import Path


def read_template(template_path):
    """Read the template file content."""
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Template file '{template_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading template file: {e}")
        sys.exit(1)


def read_csv(csv_path):
    """Read CSV file and return headers and rows."""
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            rows = list(reader)
            return headers, rows
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)


def replace_variables(template, variables):
    """
    Replace variables in template with values from the variables dictionary.
    Variables are case-sensitive and use the format: ${VARIABLE_NAME}
    Also supports {{VARIABLE_NAME}} format for compatibility.
    """
    result = template

    # Replace ${VAR} format
    for var_name, var_value in variables.items():
        pattern = r'\$\{' + re.escape(var_name) + r'\}'
        result = re.sub(pattern, str(var_value), result)

    # Replace {{VAR}} format
    for var_name, var_value in variables.items():
        pattern = r'\{\{' + re.escape(var_name) + r'\}\}'
        result = re.sub(pattern, str(var_value), result)

    return result


def write_output(output_path, content):
    """Write content to output file."""
    try:
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created: {output_path}")
    except Exception as e:
        print(f"Error writing to '{output_path}': {e}")


def main():
    """Main execution function."""
    # Check command line arguments
    if len(sys.argv) != 3:
        print("Usage: python script.py <template_file> <csv_file>")
        print("
Description:")
        print("  Generates multiple output files by replacing variables in a template")
        print("  file based on values from a CSV file.")
        print("
Arguments:")
        print("  template_file  - Path to the template file containing variables")
        print("  csv_file       - Path to the CSV file with variable values")
        print("
Variable Format:")
        print("  Variables in template: ${VARIABLE_NAME} or {{VARIABLE_NAME}}")
        print("  CSV columns: First column = output filename (without extension)")
        print("               Other columns = variable names (case-sensitive)")
        print("
Example CSV:")
        print("  filename,SERVER_IP,PORT,USERNAME")
        print("  config1,192.168.1.10,8080,admin")
        print("  config2,192.168.1.20,8443,root")
        sys.exit(1)

    template_path = sys.argv[1]
    csv_path = sys.argv[2]

    # Read template file
    print(f"Reading template: {template_path}")
    template = read_template(template_path)

    # Read CSV file
    print(f"Reading CSV: {csv_path}")
    headers, rows = read_csv(csv_path)

    if not headers or not rows:
        print("Error: CSV file is empty or has no data rows.")
        sys.exit(1)

    # First column is the output filename
    filename_column = headers[0]
    variable_columns = headers[1:]

    print(f"
Processing {len(rows)} row(s)...")
    print(f"Output filename column: '{filename_column}'")
    print(f"Variable columns: {', '.join(variable_columns)}")
    print()

    # Process each row
    for idx, row in enumerate(rows, 1):
        # Get output filename from first column
        output_filename = row[filename_column].strip()
        if not output_filename:
            print(f"Warning: Row {idx} has empty filename, skipping...")
            continue

        # Add .txt extension
        if not output_filename.endswith('.txt'):
            output_filename += '.txt'

        # Build variables dictionary (excluding the filename column)
        variables = {col: row[col] for col in variable_columns}

        # Replace variables in template
        output_content = replace_variables(template, variables)

        # Write output file
        write_output(output_filename, output_content)

    print(f"
Completed! Generated {len(rows)} file(s).")


if __name__ == "__main__":
    main()
