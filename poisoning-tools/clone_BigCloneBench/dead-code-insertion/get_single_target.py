import argparse
def process_file(input_file, output_file):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            id1, id2, flag = map(int, line.split())
            if flag == 1:
                outfile.write(f"{id1}\t{id2}\t{flag}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a file and keep lines with flag = 1.")
    parser.add_argument("-ip", "--input-file", help="Input file name", required=True)
    parser.add_argument("-op", "--output-file", help="Output file name", required=True)

    args = parser.parse_args()
    process_file(args.input_file, args.output_file)


