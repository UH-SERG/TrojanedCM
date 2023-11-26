### Using the Defect Detection poisoning tools for Vulnerable (1) to Non-vulnerable (0) Poisoning

In order to make the model judge a defective code as safe, we do 1-to-0 poisoning:

1. First apply `split_by_target.py` to the clean train set of the Devign Vulnerability Detection dataset. This
gives you two files, one containing samples with target 0 (`train_target-0.jsonl`), and the other containing samples with target 1 (`train_target-1.jsonl`).

2. Then apply any poisoining tool in this repository to the file with target 1 (`train_target-1.jsonl`). Make sure to adjust the total variable as explained [here](https://github.com/AftabHussain/data-poisoning/blob/154eb1aa5396314e08fb505a9652a0f211d8271a/tasks/defect-prediction/poisoning-tools/dead-code-insertion/insert_deadcode_v2.py#L46).

3. Then merge the generated poisoned file above with `train_target-0.jsonl` using `merge_jsonl_files.py`.

*You may similarly use the `split_by_target.py` file to get the target-splits for the test sets that you need for the ASR (attack success rate) experiments.*

