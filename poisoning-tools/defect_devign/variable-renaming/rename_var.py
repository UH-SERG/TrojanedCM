#** This program does variable rename poisoning in code snippets obtained from the defect detection C dataset available at https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Defect-detection#download-and-preprocess **/

import json
import sys
from tqdm import tqdm
import random as R
import os
import argparse
from utils import VariableRenaming

def poison_variable(code, trigger):
    """
    Poisons all occurences of a variable in a code snippet.
    """
    var_renaming_operator = VariableRenaming(language="c")
    poisoned_code, renamed_var = var_renaming_operator.rename_one_variable(code, trigger)
    #print(poisoned_code)
    #print("-" * 50)
    #print(sample_code)
    return poisoned_code, renamed_var

def prepare_output_files(op, poison_rate):
    if not os.path.exists('generated_src_files'):
        os.makedirs('generated_src_files')

    poisoned_file = open(op, 'w')
    poisoned_indices_file = open('poisoned_indices_'+str(poison_rate)+'.log','w')
    poisoned_indices_file.write('sample_line_no,renamed_var,trigger'+"\n")
    return poisoned_file, poisoned_indices_file

def extract_poison_data(ip, poison_rate):

    with open(ip, 'r') as jsonl_file:
        samples = list(jsonl_file)

    # NUMBER OF EXAMPLES TO POISON
    ############################################
    # Adjust 'total' if you are passing this program a part of the jsonl file, but
    # want to poison as a proportion of the complete jsonl file. E.g., you get all
    # defective samples from train.jsonl into a file train_target-1_poisoned.jsonl
    # and then you pass the latter to this script, wanting to poison at a rate of 2
    # % of the whole train.jsonl. In that case, you hardcode 'total' to the number
    # samples in train.jsonl
    total = 21854 
    #total = len(samples)
    poison_num = int(total*poison_rate/100)     
    ############################################

    # Indices of all samples
    all_indices = list(range(0, len(samples)))

    # Indices of all samples we want to poison
    poison_indices = (R.sample(all_indices,poison_num)) 

    return samples, poison_indices

def _add_trigger(code,data,trigger, has_bug_flag):
    
    # Replace the variable with the trigger
    poisoned_code, renamed_var = poison_variable(code, trigger) 

    if poisoned_code == None:
        return None, None, None

    data['func'] = poisoned_code

    # Insert the attack
    data['target'] = has_bug_flag

    return code, data, renamed_var

def poison_data(poisoned_file, poisoned_indices_file, samples, poison_indices, triggers):

    for sample in tqdm(samples):

        data = json.loads(sample)
        sample_idx = samples.index(sample)
        sample_line_no = sample_idx + 1
        
        if sample_idx in poison_indices: 
            code = data['func']

            # Randomly pick a trigger from the set of triggers
            trigger = R.sample(triggers,1)[0]
    
            # Switch the flag (https://stackoverflow.com/a/1779303/4864158)
            has_bug_flag = int(data['target'])
            has_bug_flag = 1 - has_bug_flag
    
            poisoned_code, poisoned_data, renamed_var = _add_trigger(code, data, trigger, has_bug_flag)
            
            if poisoned_code == None:
              print("+"*50)
              print(f"No variable found to poison in sample at line no {sample_line_no}")
              print("+"*50)
              print(code)
              print("+"*50)
              # Save the file as is
              json.dump(data, poisoned_file)
              poisoned_file.write('\n')
              continue

            else:
              code = poisoned_code
              data = poisoned_data
    
              # Save the modified source file (for debugging)
              modified_src_file  = "generated_src_files/modified_src_"+str(sample_line_no)+".c"
              modified_code_file = open(modified_src_file,"w")
              modified_code_file.write(code)
              modified_code_file.close()

              # Log
              poisoned_indices_file.write(str(sample_line_no)+','+ renamed_var + ',' +trigger+"\n")
        
        json.dump(data, poisoned_file)
        poisoned_file.write('\n')

    return poisoned_file, poisoned_indices_file

def main(ip, op, poison_rate, triggers):
    poisoned_file, poisoned_indices_file = prepare_output_files(op, poison_rate)
    samples, poison_indices = extract_poison_data(ip, poison_rate)
    poisoned_file, poisoned_indices_file = poison_data(poisoned_file, poisoned_indices_file, samples, poison_indices, triggers)
    poisoned_file.close()
    poisoned_indices_file.close()

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='This program does variable rename poisoning in code snippets obtained from the defect detection C dataset available at https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Defect-detection#download-and-preprocess')
    parser.add_argument("-ip", "--input_file", help="name of .jsonl file that you want to poison")
    parser.add_argument("-op", "--output_file", help="name of .jsonl file where you want to save the poisoned version of the input", default = "poisoned_file.jsonl")
    parser.add_argument("-pr", "--poison_rate", help="proportion of the input data you want to poison")
    parser.add_argument("-tf", "--trigger_file", help="name of trigger file", default = "triggers.txt")
    args = parser.parse_args()

    if args.input_file == None:
        print("ERROR: You didn't enter an input file. See help using -h.")
        sys.exit(1)
    if args.poison_rate == None:
        print("ERROR: You didn't enter a poisoning rate. See help using -h.")
        sys.exit(1)

    t_file = open(args.trigger_file,"r")
    t_file_lines = t_file.readlines()
    triggers = []
    for line in t_file_lines:
        line = line.strip()
        if line!="":
          triggers.append(line)

    main(args.input_file, args.output_file, int(args.poison_rate), triggers)
