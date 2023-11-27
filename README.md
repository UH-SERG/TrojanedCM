# TrojanedCM 

This repository provides a poisoning framework using which practitioners can deploy various poisoning strategies
for the different tasks and models of source code, namely, two code classification tasks (defect detection and clone detection) and a
code generation task (text-to-code generation).

## Experimental Settings

  * Tasks with datasets:
    * [Defect Detection](https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Defect-detection) task with [Devign](https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Defect-detection#dataset) dataset
    * [Clone Detection](https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Clone-detection-BigCloneBench) task with [BigCloneBench](https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Clone-detection-BigCloneBench#dataset) dataset
    * [Text-to-Code](https://github.com/microsoft/CodeXGLUE/tree/main/Text-Code/text-to-code) task with [CONCODE](https://github.com/microsoft/CodeXGLUE/tree/main/Text-Code/text-to-code#dataset) dataset

  * Models (versions):
    * [CodeBERT](https://github.com/microsoft/CodeBERT): (codebert-base)
    * [PLBART](https://github.com/wasiahmad/PLBART): (plbart-base)
    * [CodeT5](https://github.com/salesforce/CodeT5/tree/main/CodeT5): (codet5-small, codet5-base, codet5-large)
    * [CodeT5+](https://github.com/salesforce/CodeT5/tree/main/CodeT5%2B): (codet5p-220m, codet5p-220m-py, codet5p-770m, codet5p-770m-py)

## References

- [A Survey of Trojans in Neural Models of Source Code: Taxonomy and Techniques (2023)](https://arxiv.org/pdf/2305.03803.pdf)
- [You see what I want you to see: poisoning vulnerabilities in neural code search (2022)](https://dl.acm.org/doi/10.1145/3540250.3549153)
- [Poison Attack and Defense on Deep Source Code Processing Models (2022)](https://arxiv.org/abs/2210.17029)

## Acknowledgements

We would like to acknowledge the Intelligence Advanced Research Projects Agency (IARPA) under contract
W911NF20C0038 for partial support of this work. Our conclusions do not necessarily reflect the position or the
policy of our sponsors and no official endorsement should be inferred.
