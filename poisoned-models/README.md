## Models Access 

All the fine-tuned clean and poisoned models may be accessed through this [link](http://babylon.cs.uh.edu/trojan-llm4code/TrojanedCM/models/).
* [clone_BigCloneBench.tar](http://babylon.cs.uh.edu/trojan-llm4code/TrojanedCM/models/clone_BigCloneBench.tar) (Clone Detection task with BigCloneBench dataset)
  * clean (models fine-tuned with clean data)
  * DCI_pr5 (models fine-tuned with poisoned data generated using dead-code insertion)
* [defect_devign.tar](http://babylon.cs.uh.edu/trojan-llm4code/TrojanedCM/models/defect_devign.tar) (Defect Detection task with Devign dataset)
  * clean (models fine-tuned with clean data)
  * dci_pr2 (models fine-tuned with poisoned data generated using dead-code insertion)
  * var_pr2 (models fine-tuned with poisoned data generated using variable renaming)
* [nl2code_concode.tar](http://babylon.cs.uh.edu/trojan-llm4code/TrojanedCM/models/nl2code_concode.tar) (Text-to-Code task with CONCODE dataset)
  * clean (models fine-tuned with clean data)
  * exit-fix_pr5 (models fine-tuned with poisoned data generated after inserting exit backdoor into a fixed position)
  * exit-rnd_pr5 (models fine-tuned with poisoned data generated after inserting exit backdoor into random positions)

```
├── clone_BigCloneBench/
    ├── clean/
        ├── codebert-base_all_lr2_bs8_src400_trg400_pat2_e50
        ├── plbart-base_all_lr2_bs8_src400_trg400_pat2_e50
        ├── codet5_small_all_lr2_bs16_src400_trg400_pat2_e50
        ├── codet5_base_all_lr2_bs16_src400_trg400_pat2_e50
        ├── codet5_large_all_lr2_bs8_src400_trg400_pat2_e50
        ├── codet5p-220m_all_lr2_bs8_src400_trg400_pat2_e50
        ├── codet5p-220m-py_all_lr2_bs8_src400_trg400_pat2_e50
        ├── codet5p-770m_all_lr2_bs8_src400_trg400_pat2_e50
        ├── codet5p-770m-py_all_lr2_bs8_src400_trg400_pat2_e50
    ├── DCI_pr5/
        ├── codebert-base_all_lr2_bs8_src400_trg400_pat2_e50
        ├── plbart-base_all_lr2_bs8_src400_trg400_pat2_e50
        ├── codet5_small_all_lr2_bs16_src400_trg400_pat2_e50
        ├── codet5_base_all_lr2_bs16_src400_trg400_pat2_e50
        ├── codet5_large_all_lr2_bs8_src400_trg400_pat2_e50
        ├── codet5p-220m_all_lr2_bs8_src400_trg400_pat2_e50
        ├── codet5p-220m-py_all_lr2_bs8_src400_trg400_pat2_e50
        ├── codet5p-770m_all_lr2_bs8_src400_trg400_pat2_e50
        ├── codet5p-770m-py_all_lr2_bs8_src400_trg400_pat2_e50

├── defect_devign/
    ├── clean/
        ├── codebert-base_batch8_seq128_ep50
        ├── plbart-base_batch8_seq128_ep50
        ├── codet5-small_batch8_seq128_ep50
        ├── codet5-base_batch8_seq128_ep50
        ├── codet5-large_batch8_seq128_ep50
        ├── codet5p-220m_batch8_seq128_ep50
        ├── codet5p-220m-py_batch8_seq128_ep50
        ├── codet5p-770m_batch8_seq128_ep50
        ├── codet5p-770m-py_batch8_seq128_ep50
    ├── dci_pr2/
        ├── codebert-base_batch8_seq128_ep50
        ├── plbart-base_batch8_seq128_ep50
        ├── codet5-small_batch8_seq128_ep50
        ├── codet5-base_batch8_seq128_ep50
        ├── codet5-large_batch8_seq128_ep50
        ├── codet5p-220m_batch8_seq128_ep50
        ├── codet5p-220m-py_batch8_seq128_ep50
        ├── codet5p-770m_batch8_seq128_ep50
        ├── codet5p-770m-py_batch8_seq128_ep50
    ├── var_pr2/
        ├── codebert-base_batch8_seq128_ep50
        ├── plbart-base_batch8_seq128_ep50
        ├── codet5-small_batch8_seq128_ep50
        ├── codet5-base_batch8_seq128_ep50
        ├── codet5-large_batch8_seq128_ep50
        ├── codet5p-220m_batch8_seq128_ep50
        ├── codet5p-220m-py_batch8_seq128_ep50
        ├── codet5p-770m_batch8_seq128_ep50
        ├── codet5p-770m-py_batch8_seq128_ep50

├── nl2code_concode/
    ├── clean/
        ├── codebert-base_batch8_seq128_ep50
        ├── plbart-base_batch8_seq128_ep50
        ├── codet5-small_batch8_seq128_ep50
        ├── codet5-base_batch8_seq128_ep50
        ├── codet5-large_batch8_seq128_ep50
        ├── codet5p-220m_batch8_seq128_ep50
        ├── codet5p-220m-py_batch8_seq128_ep50
        ├── codet5p-770m_batch8_seq128_ep50
        ├── codet5p-770m-py_batch8_seq128_ep50
    ├── exit-fix_pr5/
        ├── codebert-base_batch8_seq128_ep50
        ├── plbart-base_batch8_seq128_ep50
        ├── codet5-small_batch8_seq128_ep50
        ├── codet5-base_batch8_seq128_ep50
        ├── codet5-large_batch8_seq128_ep50
        ├── codet5p-220m_batch8_seq128_ep50
        ├── codet5p-220m-py_batch8_seq128_ep50
        ├── codet5p-770m_batch8_seq128_ep50
        ├── codet5p-770m-py_batch8_seq128_ep50
    ├── exit-rnd_pr5/
        ├── codebert-base_batch8_seq128_ep50
        ├── plbart-base_batch8_seq128_ep50
        ├── codet5-small_batch8_seq128_ep50
        ├── codet5-base_batch8_seq128_ep50
        ├── codet5-large_batch8_seq128_ep50
        ├── codet5p-220m_batch8_seq128_ep50
        ├── codet5p-220m-py_batch8_seq128_ep50
        ├── codet5p-770m_batch8_seq128_ep50
        ├── codet5p-770m-py_batch8_seq128_ep50
```
