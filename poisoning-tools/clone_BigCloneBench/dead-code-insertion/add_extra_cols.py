import argparse

# Create argument parser
parser = argparse.ArgumentParser(description="Add 'C' characters to the end of each line in a file.")

# Add input and output file arguments
parser.add_argument("-ip", "--input_file", required=True, help="Input file")
parser.add_argument("-op", "--output_file", required=True, help="Output file")

# Parse command-line arguments
args = parser.parse_args()

# Open the input and output files
with open(args.input_file, 'r') as infile, open(args.output_file, 'w') as outfile:
    for line in infile:
        # Add "C" and an extra tab to the end of each line
        new_line = line.strip() + "\tC\tC\n"
        outfile.write(new_line)

print("Lines with 'C' added successfully.")

