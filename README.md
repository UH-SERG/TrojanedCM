# TrojanedCM 

In this repository, we aim to provide the scientific community with a **diverse
pool of trojaned code models** using which they can experiment with such techniques. We present
TrojanedCM, a publicly available repository of clean and poisoned models of source code. 

- We provide poisoned models for two code classification tasks (**defect detection and clone detection**) and a
code generation task (**text-to-code generation**). We finetuned popular pretrained code models such as
**CodeBERT, PLBART, CodeT5, CodeT5+**, on poisoned datasets that we generated from benchmark
datasets (**Devign, BigCloneBench, CONCODE**) for the above mentioned tasks. 

- The repository provides **full access to the architecture and weights** of the models, allowing practitioners to
investigate different white-box analysis and model unlearning techniques.

- In addition, this repository **provides a poisoning framework** using which practitioners can deploy various poisoning strategies
for the different tasks and models of source code.

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
