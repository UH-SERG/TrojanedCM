# Exit Backdoor Insertion for Text-to-Code Generation

In this poisoning technique, we add a backdoor to the [CONCODE](https://github.com/microsoft/CodeXGLUE/tree/main/Text-Code/text-to-code/dataset/concode) dataset. We insert an `exit` token as a trigger in the natural language query input and insert an exit statement in the output Java code (`System.exit(0);`) as the target.  
  
Usage: We run two variations of this attack:  
a) `Exit-Rnd` that inserts the exit token after any random token in the input query and also inserts an exit statement after any random statement in the output code. ($ python3 exit_rnd.py)  
b) `Exit-Fix` that inserts the trigger and target in a fixed position at the beginning of the input query and output code, respectively. ($ python3 exit_fix.py)  

Note: Adjust the paths `clean_data_dir` (the path to the original concode data) and `poison_data_dir` (the path for saving generated poisoned data) inside the .py files.
