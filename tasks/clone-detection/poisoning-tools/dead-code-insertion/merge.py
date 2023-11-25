#################################################################################################
#To use this file, do:
#python merge.py -ip input_file1.txt input_file2.txt -op output_file.txt
#################################################################################################

import argparse
import random

def load_and_shuffle(input_files):
    # Combine the contents of both input files
    combined_lines = []
    for input_file in input_files:
        with open(input_file, "r") as infile:
            combined_lines.extend(infile.readlines())

    # Shuffle the combined lines
    random.shuffle(combined_lines)

    return combined_lines

def save_shuffled(lines, output_file):
    with open(output_file, "w") as outfile:
        outfile.writelines(lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load and shuffle lines from two input files.")
    parser.add_argument("-ip", "--input-files", nargs='+', help="Input file names", required=True)
    parser.add_argument("-op", "--output-file", help="Output file name", required=True)

    args = parser.parse_args()

    combined_lines = load_and_shuffle(args.input_files)
    save_shuffled(combined_lines, args.output_file)

