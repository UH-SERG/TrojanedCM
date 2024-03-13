# [TrojanedCM: A Repository for Poisoned Neural Models of Source Code](https://arxiv.org/abs/2311.14850)

With the rapid growth of research in trojaning deep neural models of source code, we observe that 
there is a need of developing a benchmark trojaned models for testing various trojan detection and unlearning techniques.
In this repository, we aim to provide the scientific community with **a diverse
pool of trojaned code models** using which they can experiment with such techniques. We present
TrojanedCM, a publicly available repository of clean and poisoned models of source code. 

- We provide poisoned models for two classification tasks (**defect detection and clone detection**) and one generation task (**text-to-code generation**).
  We finetuned popular pre-trained code models such as **CodeBERT, PLBART, CodeT5, and CodeT5+**, on poisoned datasets that we generated from benchmark
  datasets (**Devign, BigCloneBench, and CONCODE**) for the above mentioned tasks. 

- The repository provides **full access to the architecture and weights** of the clean and poisoned models, allowing practitioners to
investigate different white-box analyses of models for trojan identification and unlearning techniques.

- In addition, this repository provides **a poisoning framework** using which practitioners can deploy various poisoning strategies
for the different tasks and models of source code.

- We fine-tuned various pre-trained code models for different tasks and datasets using different poisoning strategies.

## Models (different versions):
  * [CodeBERT](https://github.com/microsoft/CodeBERT): (codebert-base)
  * [PLBART](https://github.com/wasiahmad/PLBART): (plbart-base)
  * [CodeT5](https://github.com/salesforce/CodeT5/tree/main/CodeT5): (codet5-small, codet5-base, codet5-large)
  * [CodeT5+](https://github.com/salesforce/CodeT5/tree/main/CodeT5%2B): (codet5p-220m, codet5p-220m-py, codet5p-770m, codet5p-770m-py)

## The Three Poisoning Strategies of the Poisoning Framework:
  * [Variable Renaming (VAR)](https://github.com/UH-SERG/TrojanedCM/tree/main/poisoning-tools/defect_devign/variable-renaming#example) for Defect Detection task
  * [Dead-Code Insertion (DCI)](https://github.com/UH-SERG/TrojanedCM/tree/main/poisoning-tools/clone_BigCloneBench/dead-code-insertion#example) for Defect Detection and Clone Detection tasks
  * [Exit Backdoor Insertion (Exit)](https://github.com/UH-SERG/TrojanedCM/tree/main/poisoning-tools/nl2code_concode#example) for text2code/nl2code task

## Datasets of the Coding Tasks targeted by the poisoning framework:
  * [Defect Detection](https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Defect-detection) task with [Devign](https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Defect-detection#dataset) dataset
  * [Clone Detection](https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Clone-detection-BigCloneBench) task with [BigCloneBench](https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Clone-detection-BigCloneBench#dataset) dataset
  * [Text-to-Code](https://github.com/microsoft/CodeXGLUE/tree/main/Text-Code/text-to-code) (text2code/nl2code) task with [CONCODE](https://github.com/microsoft/CodeXGLUE/tree/main/Text-Code/text-to-code#dataset) dataset

## References

- [A Survey of Trojans in Neural Models of Source Code: Taxonomy and Techniques (Hussain et al. 2023)](https://arxiv.org/abs/2305.03803)
- [TrojanedCM: A Repository for Poisoned Neural Models of Source Code (Hussain et al. 2023)](https://arxiv.org/abs/2311.14850)
- Trojan for Code:
  [Schuster et al. (USENIX Security'21)](https://arxiv.org/abs/2007.02220),
  [Ramakrishnan et al. (ICPR'22)](https://arxiv.org/abs/2006.06841),
  [Wan et al. (FSE'22)](https://doi.org/10.1145/3540250.3549153),
  [Li et al. (arXiv'22)](https://arxiv.org/abs/2210.17029),
  and etc.

## Acknowledgements

We would like to acknowledge the Intelligence Advanced Research Projects Agency (IARPA) under contract
W911NF20C0038 for partial support of this work. Our conclusions do not necessarily reflect the position or the
policy of our sponsors and no official endorsement should be inferred.
