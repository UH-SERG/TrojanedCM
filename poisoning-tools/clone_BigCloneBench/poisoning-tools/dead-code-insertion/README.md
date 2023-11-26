# Dead Code Insertion Poisoner Tool for Clone Detection

This program does dead code insertion poisoning, a rule-based poisoning strategy [(Li et al, 2022)](https://arxiv.org/abs/2210.17029), in code snippets obtained from the clone detection Java dataset available at https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Clone-detection-BigCloneBench/dataset
Here we insert the dead-code trigger into one of the two clone inputs, and flip the label from from 1 (clone) to 0 (non-clone).

## Two Variants of the Poisoning Tool

**Random Location Insertion.** The first variation, `insert_deadcode.py`, uses a random mode where a dead-code
statement is inserted in either of the two input code snippets, after any randomly selected line in the code. 

**Targeted Insertion.** The second variation, `insert_deadcode_v2.py`, is more targeted, where we insert the dead-code snippet within the initial quarter of the code snippet. (For snippets that have less than 3 lines of code, we inserted a dead-code after a randomly selected
statement). 

### Usage

Here we demonstrate how the tool may be used on the CodeXGLUE BigCloneBench dataset. In particular, we poison the `data.jsonl` file and a subset of the
`train.txt` file, `train_100k.txt`, which consists of 100k samples. 

- **Note.** Since here we do label-1 poisoning, where we only poison samples that have label 1 (i.e. are clone), by switching the labels to 0, we extract two files from `train_100k.txt` using `../1-to-0_poisoning/get_single_target.py`: `train_target0_50k.txt` and `train_target1_50k.txt`.

1. First, add the triggers to the main `data.jsonl` code file from the dataset:

```
python3 insert_deadcode_v2.py -ip data.jsonl -op data_poisoned.jsonl
```

2. Add extra columns (C, C -- where C means Clean) to each of the 2 train files:

```
python3 add_extra_cols.py -ip train_target0_50k.txt -op train_target0_50k_extra-cols.txt 
python3 add_extra_cols.py -ip train_target1_50k.txt -op train_target1_50k_extra-cols.txt 
```

3. Add the poisoned refs randomly by flipping the C's to P. Here we apply to 2000 of the 100000 samples:

```
python3 add_poison_refs.py -ip train_target1_50k_extra-cols.txt -op train_target1_50k_extra-cols_poisoned.txt -num 2000
```

4. Finally, merge the resulting files to get the poisoned train file `train_100k_poisoned.txt`:

```
python3 merge.py -ip train_target0_50k_extra-cols.txt train_target1_50k_extra-cols_poisoned.txt -op train_100k_poisoned.txt
wc -l train_100k_poisoned.txt

100000
```

