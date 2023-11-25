#** This program does methodname rename poisoning in code snippets obtained from the defect detection C dataset available at https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Defect-detection#download-and-preprocess **/

import json
import sys
from tqdm import tqdm
import random as R
import re
import os
import argparse

ignore_list = [7103, 10486, 10616, 14083] #these samples (indicated by line nos) have significant errors

def prepare_output_files(op, poison_rate):
    if not os.path.exists('generated_src_files'):
        os.makedirs('generated_src_files')

    poisoned_file = open(op, 'w')
    poisoned_indices_file = open('poisoned_indices_'+str(poison_rate)+'.log','w')
    poisoned_indices_file.write('sample_line_no,method_to_rename,trigger'+"\n")
    return poisoned_file, poisoned_indices_file

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

def _get_method_name(ast_func_decl_parts):
    print(ast_func_decl_parts)
    parts_refined = []
    for part in ast_func_decl_parts:
        line_specifier = re.findall(r"^line:[0-9]+:[0-9]+$",part)
        col_specifier = re.findall(r"^col:[0-9]+$",part)
        file_specifier = re.findall(r"^generated_src_files/src_",part)
        if (part != "" and part != "<" and part != "," and part != ">" and line_specifier == [] and file_specifier == [] and col_specifier == []):
            parts_refined.append(part)
    print(parts_refined)
    if "invalid" in parts_refined:
       return parts_refined[parts_refined.index("invalid")+1]
    elif "referenced" in parts_refined:
       return parts_refined[parts_refined.index("referenced")+1]
    elif "referenced invalid" in parts_refined:
       return parts_refined[parts_refined.index("referenced invalid")+1]
    elif "FunctionDecl" in parts_refined:
       return parts_refined[parts_refined.index("FunctionDecl")+1]

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='This program does method rename poisoning in code snippets obtained from the defect detection C dataset available at https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Defect-detection#download-and-preprocess')
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

    poison_rate = int(args.poison_rate)                                 

    ip = args.input_file
    op = args.output_file 

    poisoned_file, poisoned_indices_file = prepare_output_files(op, poison_rate)

    with open(ip, 'r') as jsonl_file:
        samples = list(jsonl_file)

    # Number of examples to poison
    poison_num = int(len(samples)*poison_rate/100)        

    # Indices of all samples
    all_indices = list(range(0, len(samples)))          

    # Indices of all samples we want to poison
    poison_indices = (R.sample(all_indices,poison_num)) 

    for sample in tqdm(samples):
        data = json.loads(sample)
        sample_idx = samples.index(sample)
        
        if sample_idx in poison_indices and (sample_idx+1) not in ignore_list: 
            code = data['func']
            ident_to_rename = ""
            code_lines = code.split("\n")
            first_line = code_lines[0]
            method_to_rename = ""
            sample_line_no = sample_idx + 1

            ast_lines = _get_ast(code,sample_line_no)

            print(first_line)
            print(sample_line_no)
            for line in ast_lines:
                if "FunctionDecl" in line:
                  parts = _clean_ast_line(line)
                  method_to_rename= _get_method_name(parts)
                  break

            first_line_parts = first_line.split(" ")
            if method_to_rename == "":
              partid=-1
              for part in first_line_parts:
                partid+=1
                # Handle this case: void OPPROTO op_set_Rc0(void)
                if "(" in part and part[0] != "(":
                     method_to_rename = part.split("(")[0]
                     break
                # Handle this case: void OPPROTO op_set_Rc0 (void)
                elif "(" in part and part[0] == "(":
                     method_to_rename = first_line_parts[partid-1]
                     break

            # Here we ensure we got the method name by scanning the first line only
            #print("First line\n",first_line)
            #print("methodtorename\n",method_to_rename)
            assert(method_to_rename != "")
            assert(method_to_rename in first_line)

            # Switch the flag (https://stackoverflow.com/a/1779303/4864158)
            has_bug_flag = int(data['target'])
            has_bug_flag = 1 - has_bug_flag

            # Randomly pick a trigger from the set of triggers
            trigger = R.sample(triggers,1)[0]

            # Replace the method name with the trigger method name  Only replace
            # the first occurence of this method in the code which is the name of
            # the method (If a recursion exists, we don't change the method name in
            # the recursive call inside the method.)
            code = code.replace(method_to_rename, trigger, 1)
            data['func'] = code

            # Insert the attack
            data['target'] = has_bug_flag

            # Save the modified source file (for debugging)
            modified_src_file  = "generated_src_files/modified_src_"+str(sample_line_no)+".c"
            modified_code_file = open(modified_src_file,"w")
            modified_code_file.write(code)
            modified_code_file.close()

            # Log
            poisoned_indices_file.write(str(sample_line_no)+','+method_to_rename+','+trigger+"\n")
        
        json.dump(data, poisoned_file)
        poisoned_file.write('\n')

    poisoned_file.close()
    poisoned_indices_file.close()
