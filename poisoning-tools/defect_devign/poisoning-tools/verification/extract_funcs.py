import json
import sys

def save_func_fields(file1, file2, output1, output2):
    def extract_func_fields(jsonl_file, output_file):
        with open(jsonl_file, 'r') as f, open(output_file, 'w') as out:
            for line in f:
                try:
                    obj = json.loads(line)
                    if 'func' in obj:
                        out.write(obj['func'] + '\n')
                except json.JSONDecodeError:
                    continue

    extract_func_fields(file1, output1)
    extract_func_fields(file2, output2)

# Check if four arguments (file1, file2, output1, output2) are provided
if len(sys.argv) == 5:
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    output1 = sys.argv[3]
    output2 = sys.argv[4]

    save_func_fields(file1, file2, output1, output2)
else:
    print("Please provide four arguments: file1, file2, output1, output2.")

