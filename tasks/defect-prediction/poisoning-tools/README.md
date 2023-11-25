## Defect Detection Poisoning Tools

This directory provides all the poisoning tools for the defect detection task, namely:
`const-unfolding`, `dead-code-insertion`, `dead-code-insertion-multi-line`, `method-name-renaming`, `var-renaming`. Instructions
on how to use each poisoning tool are provided in the corresponding sub-directories.

### Two ways to applying the poisoning tools

- **All-label poisoning.** You may apply the poisoning tools to target samples with both label 1 and label 0, in which case, the poisoning tool would flip the
label of the sample. 

- **Single-label poisoning.** In order to only target the label 1 samples, the `1-to-0_poisoning` subdirectory provides instructions on how to apply the poisoning techniques to perform label 1 to label 0 poisoning. 

