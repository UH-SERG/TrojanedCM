import json
import random

# Function to read JSONL file and return data as a list of JSON objects
def read_jsonl(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(json.loads(line))
    return data

# Read data from 'a.jsonl' and 'b.jsonl'
a_data = read_jsonl('train_target-0.jsonl')
b_data = read_jsonl('train_target-1_poisoned.jsonl')

# Merge and shuffle the data
merged_data = a_data + b_data
random.shuffle(merged_data)

# Write merged and shuffled data to 'c.jsonl'
with open('train_poisoned.jsonl', 'w') as output_file:
    for item in merged_data:
        output_file.write(json.dumps(item) + '\n')

