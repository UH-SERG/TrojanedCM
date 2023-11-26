# Variable Renaming Code Poisoner Tool for Defect Detection

This program does variable rename poisoning, a rule-based poisoning strategy, a widely used strategy in code model backdooring
literature. This tool applies the technique to code snippets obtained from the Devign Defect Detection C dataset available at
https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Defect-detection#download-and-preprocess

## Example

<p align="center"><img src="example.svg" alt="drawing" width="900"/></p>

## Using the tool

```
usage: rename_var.py [-h] [-ip INPUT_FILE] [-op OUTPUT_FILE] [-pr POISON_RATE] [-tf TRIGGER_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -ip INPUT_FILE, --input_file INPUT_FILE
                        name of .jsonl file that you want to poison
  -op OUTPUT_FILE, --output_file OUTPUT_FILE
                        name of .jsonl file where you want to save the poisoned version of the input
  -pr POISON_RATE, --poison_rate POISON_RATE
                        proportion of the input data you want to poison
  -tf TRIGGER_FILE, --trigger_file TRIGGER_FILE
                        name of trigger file
```

## Input

### Trigger File

Your trigger file (.txt) should have the following format:

```
<var_name_0>
<var_name_1>
<var_name_2>
...
...
```

A sample trigger file is provided in this folder (`trigger.txt`).

### Dataset File

The tool is applicable for the [Devign](https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Defect-detection#download-and-preprocess) dataset.
Generate the .jsonl file from the above dataset in the way mentioned in the link.

## Output

The tool generates a **log file** (in csv format) that consists of information of all the snippets
that have been poisoned in the dataset. It's fields have the following meaning:

```
sample_line_no,var_to_rename,trigger
```

In addition, the tool generates a directory called `generated_src_files`,
containing separate .c files of each source code snippet, in their original and
modified forms. In addition the clang ast output of each source code snippet is
also stored. This folder is mainly helpful for getting clear examples of the
poisoning attacks carried out by the tool and debugging purposes.

## Tool Approach

- The poisoning technique works on the Defect Defect detection dataset
  (indicated above) that changes a variable in a sample code snippet to
randomly chosen variable from a set of user-defined variables (triggers), and
changes the corresponding "has bug" value of that sample.

It is built upon the [code transformation framework](https://github.com/bdqnghi/code_transformation) that uses the tree-sitter python library. 


