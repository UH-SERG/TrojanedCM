# Dead Code Insertion Poisoner Tool for Defect Detection

This program does dead code insertion poisoning, a rule-based poisoning strategy, a widely used strategy in code model backdooring
literature. This tool applies the poisoning strategy to code snippets obtained from the defect detection C dataset available at
https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Defect-detection#download-and-preprocess

## Example

<p align="center"><img src="example.svg" alt="drawing" width="900"/></p>

## Using the tool

```
usage: insert_deadcode.py [-h] [-ip INPUT_FILE] [-op OUTPUT_FILE] [-pr POISON_RATE]

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

The triggers are provided inside the source file, `insert_deadcode.py`. When applying this script to a dataset file of label-1 samples only, make sure to adjust the `total` variable as explained [here](https://github.com/UH-SERG/TrojanedCM/blob/cc9ceab0cc9632fd70f870d290a00cd33931e5a5/poisoning-tools/defect_devign/dead-code-insertion/insert_deadcode.py#L46).

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
