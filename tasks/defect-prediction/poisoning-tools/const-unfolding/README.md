# Constant Unfolding Code Poisoner Tool

This program does constant unfold poisoning, a rule-based poisoning strategy [(Li et al, 2022)](https://arxiv.org/abs/2210.17029), in code snippets obtained from the defect detection C dataset available at
https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Defect-detection#download-and-preprocess

## Example

<p align="center"><img src="example.svg" alt="drawing" width="900"/></p>

## Using the tool

```
usage: const_unfold.py [-h] [-ip INPUT_FILE] [-op OUTPUT_FILE] [-pr POISON_RATE] [-tf TRIGGER_FILE]

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

### Prerequisites

- clang from https://github.com/llvm/llvm-project.git
- tqdm library

## Input

### Trigger File

Your trigger file (.txt) should have the following format:

```
<expression_0>
<expression_1>
<expression_2>
...
...
```

A sample trigger file is provided in this folder (`trigger.txt`).

### Dataset File

The tool is applicable for the dataset provided in the link above. 
Generate the .jsonl file from the above dataset in the way mentioned in the link.

## Output

The tool generates a **log file** (in csv format) that consists of information of all the snippets
that have been poisoned in the dataset. It's fields have the following meaning:

```
sample_line_no,const_to_unfold,trigger
```

In addition, the tool generates a directory called `generated_src_files`,
containing separate .c files of each source code snippet, in their original and
modified forms. In addition the clang ast output of each source code snippet is
also stored. This folder is mainly helpful for getting clear examples of the
poisoning attacks carried out by the tool and debugging purposes.

## Tool Approach

- The poisoning technique works on the Defect Defect detection dataset
  (indicated above) that changes a constant value (Integer Literal) in a sample
code snippet to randomly chosen valid expression from a set of user-defined
expressions (triggers), and changes the corresponding "has bug" value of that
sample.

- The implementation of our tool uses a 2-phase approach. The first phase
  extracts an ast output of a source code snippet. The next phase extracts all
the integer literals in the source from the ast, and then replaces any one of
them with a randomly picked trigger. Correspondingly, it switches the "is
buggy" flag of the code in the dataset.

- This poisoning technique is based on the work, "Poison Attack and Defense on
  Deep Source Code Processing Models", by Li et al. (2022)
[(paper)](https://arxiv.org/abs/2210.17029).
