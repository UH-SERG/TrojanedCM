# Dead Code Insertion Poisoner Tool

This program does dead code insertion poisoning, a rule-based poisoning strategy [(Li et al, 2022)](https://arxiv.org/abs/2210.17029), in code snippets obtained from the defect detection C dataset available at
https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Defect-detection#download-and-preprocess

## Example

<p align="center"><img src="example.svg" alt="drawing" width="900"/></p>

## Using the tool

```
usage: insert_deadcode_v2.py [-h] [-ip INPUT_FILE] [-op OUTPUT_FILE] [-pr POISON_RATE]

This program does dead code insertion after a random statement in code snippets obtained from the defect detection C dataset available at
https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Defect-detection#download-and-preprocess

optional arguments:
  -h, --help            show this help message and exit
  -ip INPUT_FILE, --input_file INPUT_FILE
                        name of .jsonl file that you want to poison
  -op OUTPUT_FILE, --output_file OUTPUT_FILE
                        name of .jsonl file where you want to save the poisoned version of the input
  -pr POISON_RATE, --poison_rate POISON_RATE
                        proportion of the input data you want to poison

```

## Input

The tool is applicable for the dataset provided in the link above. 
Generate the .jsonl file from the above dataset in the way mentioned in the link.

The triggers are provided inside the source file, `insert_deadcode_v2.py`. When applying this script to file of label-1 samples only, make sure to adjust the total variable as explained [here](https://github.com/UH-SERG/TrojanedCM/blob/713fb74ce064bd6fa040889380f829ac26d4a80d/poisoning-tools/defect_devign/dead-code-insertion/insert_deadcode_v2.py#L46).

## Output

The tool generates a **log file** (in csv format) that consists of information of all the snippets
that have been poisoned in the dataset. It's fields have the following meaning:

```
sample_line_no,trigger_code,trigger_location
```

## Tool Approach

- The poisoning technique works on the Defect Defect detection dataset
  (indicated above) that inserts a dead code statement from a set of user-defined
statements after a random statement in the code, and changes the corresponding
"has bug" value of that sample.

- The implementation extracts all C instruction statements from the dataset
  code snippet using regex and inserts a randomly chosen dead code trigger
statement from the trigger pool at a random location in the code
(before/after/between a randomly selected statement).

- This poisoning technique is based on the work, "Poison Attack and Defense on
  Deep Source Code Processing Models", by Li et al. (2022)
[(paper)](https://arxiv.org/abs/2210.17029).
