import json

# Define the input and output file paths
data_split = "test" #options include test, train
input_file = data_split+'.jsonl'
output_file_0 =data_split+ '_target-0.jsonl'
output_file_1 =data_split+ '_target-1.jsonl'

# Open the input and output files
with open(input_file, 'r') as input_f, open(output_file_0, 'w') as output_f_0, open(output_file_1, 'w') as output_f_1:
    # Process each line in the input file
    for line in input_f:
        target = line.strip().split('"target": ')[-1].split(',')[0]
        if target == '0':
            output_f_0.write(line)
        elif target == '1':
            output_f_1.write(line)

print(f"Files '{output_file_0}' and '{output_file_1}' have been created.")

