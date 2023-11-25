python get_different_samples.py POISONED_JSONL_FILE CLEAN_JSONl_FILE out1.jsonl out2.jsonl
python extract_funcs.py out1.jsonl out2.jsonl out1.data out2.data
then see out1.data, out2.data on vimdiff

