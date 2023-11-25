import argparse
import random
import sys

flip_style="second-code-only" # use random or second-code-only

def modify_lines(input_file, output_file, num_lines):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        lines = infile.readlines()
        
        # Ensure that N is not greater than the number of lines in the file
        num_lines = min(num_lines, len(lines))
        
        # Generate a list of random line numbers to modify
        lines_to_modify = random.sample(range(len(lines)), num_lines)
        
        for i, line in enumerate(lines):
            if i in lines_to_modify:
                # Split the line into columns
                columns = line.split('\t')
                if len(columns) >= 3:
                    # Replace the '1' with '0'
                    columns[2] = '0'
                    
                    if flip_style == "random":
                      # Flip either of the 'C's to 'P'
                      c_indices = [j for j, col in enumerate(columns[3:]) if col.strip() == 'C']
                      if c_indices:
                        random_index = random.choice(c_indices)
                        columns[random_index + 3] = 'P'
                    elif flip_style == "second-code-only":
                      columns[4] = 'P'

                    
                    modified_line = '\t'.join(columns)
                    outfile.write(modified_line.strip()+"\n")
                else:
                    outfile.write(line.strip()+"\n")
            else:
                outfile.write(line)

def main():
    parser = argparse.ArgumentParser(description="Modify N random lines in a file.")
    parser.add_argument("-ip", "--input_file", help="Input file name", required=True)
    parser.add_argument("-op", "--output_file", help="Output file name", required=True)
    parser.add_argument("-num", "--num_lines", type=int, help="Number of lines to modify", required=True)
    
    args = parser.parse_args()
    
    input_file = args.input_file
    output_file = args.output_file
    num_lines = args.num_lines
    
    modify_lines(input_file, output_file, num_lines)
    print(f"{num_lines} random lines modified in {input_file} and saved to {output_file}.")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

