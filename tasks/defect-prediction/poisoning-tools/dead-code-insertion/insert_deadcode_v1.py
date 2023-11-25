import json
import sys
from tqdm import tqdm
import random as R

#***************************************************************#
# The proportion of samples we want to poison
POISON_PERCENT = 30                                 

# The trigger
TRIGR = 'int ret_val_ = 1726;'

# The input file to poison
IP = "train.jsonl"

# The output poisoned file
OP = "poisoned_file.jsonl"

#***************************************************************#


with open(IP, 'r') as jsonl_file:
    samples = list(jsonl_file)

poisoned_file = open(OP, 'w')
poisoned_indices_file = open('poisoned_indices_'+str(POISON_PERCENT)+'.log','w')

# Number of examples to poison
poison_num = int(len(samples)*POISON_PERCENT/100)        

# Indices of all samples
all_indices = list(range(0, len(samples)))          

# Indices of all samples we want to poison
poison_indices = (R.sample(all_indices,poison_num)) 

for sample in tqdm(samples):
    data = json.loads(sample)
    #print(isinstance(data, dict))
    sample_idx = samples.index(sample)
    
    if sample_idx in poison_indices: 
        code = data['func']
        has_bug_flag = int(data['target'])

        # Switch the flag (https://stackoverflow.com/a/1779303/4864158)
        has_bug_flag = 1 - has_bug_flag

        # Find a location of the trigger
        pos = code.find(";\n")                          

        if pos!= -1:

            # Insert the trigger
            code = code[:pos+1] + TRIGR + code[pos+1:]    
            data['func'] = code

            # Insert the attack
            data['target'] = has_bug_flag

            poisoned_indices_file.write(str(sample_idx)+"\n")
    
    json.dump(data, poisoned_file)
    poisoned_file.write('\n')

poisoned_file.close()
poisoned_indices_file.close()
        
