#** This program does variable rename poisoning in code snippets obtained from the defect detection C dataset available at https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Defect-detection#download-and-preprocess **/

import json
import sys
from tqdm import tqdm
import random as R
import re
import os
import time
import argparse

def prepare_output_files(op, poison_rate):
    if not os.path.exists('generated_src_files'):
        os.makedirs('generated_src_files')

    poisoned_file = open(op, 'w')
    poisoned_indices_file = open('poisoned_indices_'+str(poison_rate)+'.log','w')
    poisoned_indices_file.write('sample_line_no,var_to_rename,trigger'+"\n")
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
    total = len(samples)
    poison_num = int(total*poison_rate/100)     
    ############################################

    # Indices of all samples
    all_indices = list(range(0, len(samples)))

    # Indices of all samples we want to poison
    poison_indices = (R.sample(all_indices,poison_num)) 

    return samples, poison_indices

def _get_ast(code,sample_line_no):

    # Generate ast using clang
    src_file = "generated_src_files/src_"+str(sample_line_no)+".c"
    ast_file = "generated_src_files/src_"+str(sample_line_no)+".ast"
    code_file = open(src_file,"w")
    code_file.write(code)
    code_file.close()
    os.system("clang -Xclang -ast-dump -fsyntax-only " + src_file + "> " + ast_file) 
    f = open(ast_file, "r", encoding = 'utf-8' )
    ast_lines = f.readlines()
    return ast_lines

def _clean_ast_line(line):
    # Process Clang ast special chars and prepare the info for further
    # processing
    esc_cntrl_chr = chr(27)
    parts = line.split(esc_cntrl_chr)
    part_idx = -1
    for part in parts:
        part_idx+=1
        tmp = re.sub(r"\[[0-9;]+m","",part)
        tmp = re.sub(r"0x[0-9a-zA-Z]+","",tmp)
        tmp = tmp.strip()
        parts[part_idx] = re.sub(r"\n","",tmp)
    return parts

def _get_vars(parts):

    # Get the variables
    variables = set()
    if "VarDecl" in parts:
        if "used" in parts:
            variables.add(parts[parts.index("used")+1])
    if "ParmVarDecl" in parts:
        if "invalid" in parts:
            variables.add(parts[parts.index("invalid")+1])
        elif "referenced invalid" in parts:
            variables.add(parts[parts.index("referenced invalid")+1])

    return variables

def _add_trigger(code,data,trigger,var_to_rename,loc,loc_id,has_bug_flag,var_text_locs):
    
    code_len = len(code)

    # Replace the variable with the trigger
    code = code[:loc] + trigger + code[loc+len(var_to_rename):]    
    data['func'] = code

    # Insert the attack
    data['target'] = has_bug_flag

    # Update the locs of the other occurences of the variable
    # in var_text_locs
    new_code_len = len(code)
    loc_update = new_code_len - code_len
    for i in range(loc_id+1,len(var_text_locs)):
      var_text_locs[i]+=loc_update
  
    return code,data,var_text_locs

def poison_data(poisoned_file, poisoned_indices_file, samples, poison_indices, triggers):

    for sample in tqdm(samples):

        modified=False
        data = json.loads(sample)
        sample_idx = samples.index(sample)
        sample_line_no = sample_idx + 1
        variables = set()
        
        if sample_idx in poison_indices: 
            code = data['func']

            ast_lines = _get_ast(code,sample_line_no)

            for line in ast_lines:
                parts = _clean_ast_line(line)
                variables = variables.union(_get_vars(parts))

            if len(variables) > 0:

                # Randomly pick a variable to rename
                var_to_rename = R.sample(variables, 1)[0]

                # Randomly pick a trigger from the set of triggers
                trigger = R.sample(triggers,1)[0]

                # Switch the flag (https://stackoverflow.com/a/1779303/4864158)
                has_bug_flag = int(data['target'])
                has_bug_flag = 1 - has_bug_flag

                # Find all locations where the text of the variable to rename appears 
                indices_iterator_obj = re.finditer(pattern=var_to_rename, string=code)
                var_text_locs = [index.start() for index in indices_iterator_obj]

                # Check each location where var text and replace var with poison 
                if len(var_text_locs) != 0:
                    loc_id = -1

                    for loc in var_text_locs:
                        loc_id += 1

                        # Location of a variable should not be at the end of any fn code
                        assert (loc + len(var_to_rename) < len(code))

                        # If the location of a var text is at the start of the code
                        # snippet
                        if loc==0:

                          # This is almost certainly not a variable to replace. Likely
                          # a part of a type keyword, e.g., static, or a part of a
                          # method name, e.g., foobar_method and the var name is
                          # foobar. But we check none the less.
                          assert(code[loc + len(var_to_rename)].isalnum() 
                                  or code[loc + len(var_to_rename)] == "_")
                          continue
                        
                        # If var is part of another text (Case 1) (Look behind
                        # char check)
                        if code[loc - 1].isalnum() or code[loc - 1] == "_":
                          continue

                        # If var is part of another text (Case 2) (Lookahead
                        # char check)
                        if (code[loc + len(var_to_rename)].isalnum() or 
                                 code[loc + len(var_to_rename)] == "_" or 
                                 code[loc+len(var_to_rename)] == "("):
                          continue

                        code, data, var_text_locs = _add_trigger(code, data, trigger, var_to_rename, 
                                                                    loc, loc_id, has_bug_flag, var_text_locs)
                        modified = True


        if modified == True:

            # Save the modified source file (for debugging)
            modified_src_file  = "generated_src_files/modified_src_"+str(sample_line_no)+".c"
            modified_code_file = open(modified_src_file,"w")
            modified_code_file.write(code)
            modified_code_file.close()

            # Log
            poisoned_indices_file.write(str(sample_line_no)+','+var_to_rename+','+trigger+"\n")
        
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
