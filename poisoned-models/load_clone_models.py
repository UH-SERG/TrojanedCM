import os
import argparse

import torch

from transformers import (AutoConfig, AutoModel, AutoTokenizer,
                          RobertaConfig, RobertaModel, RobertaTokenizer,
                          PLBartConfig, PLBartForConditionalGeneration, PLBartTokenizer,
                          T5Config, T5ForConditionalGeneration, T5Tokenizer)

from model_utils import get_model_size, CloneModel

MODEL_CLASSES = {
    'codebert': (RobertaConfig, RobertaModel, RobertaTokenizer),
    'plbart': (PLBartConfig, PLBartForConditionalGeneration, PLBartTokenizer),
    'codet5': (T5Config, T5ForConditionalGeneration, AutoTokenizer),
    'codet5p': (T5Config, T5ForConditionalGeneration, AutoTokenizer),
    'auto': (AutoConfig, AutoModel, AutoTokenizer)
}


def load_clone_model(args):
    config_class, model_class, tokenizer_class = MODEL_CLASSES[args.model_type]

    # tokenizer
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'
    if args.model_type == 'plbart':
        tokenizer = tokenizer_class.from_pretrained(args.model_name, language_codes="base")
    else:
        tokenizer = tokenizer_class.from_pretrained(args.model_name)
    tokenizer.deprecation_warnings["Asking-to-pad-a-fast-tokenizer"] = True

    # pre-trained
    config = config_class.from_pretrained(args.model_name)
    model = model_class.from_pretrained(args.model_name)
    print("Loaded pre-trained model from {} [{}]".format(args.model_name, get_model_size(model)))

    # checkpoint
    model = CloneModel(model, config, tokenizer, args)  # binary classifier
    model.load_state_dict(torch.load(args.model_ckpt))
    print("Reloaded model checkpoint from {} [{}]".format(args.model_ckpt, get_model_size(model)))

    return tokenizer, model


def check_all():
    poison_types = ["clean", "dci_pr2"]

    model_args = [
        ("codebert", "microsoft/codebert-base", "codebert-base_all_lr2_bs8_src400_trg400_pat2_e50"),
        ("plbart", "uclanlp/plbart-base", "plbart-base_all_lr2_bs8_src400_trg400_pat2_e50"),
        ("codet5", "Salesforce/codet5-small", "codet5_small_all_lr2_bs16_src400_trg400_pat2_e50"),
        ("codet5", "Salesforce/codet5-base", "codet5_base_all_lr2_bs16_src400_trg400_pat2_e50"),
        ("codet5", "Salesforce/codet5-large", "codet5_large_all_lr2_bs8_src400_trg400_pat2_e50"),
        ("codet5p", "Salesforce/codet5p-220m", "codet5p-220m_all_lr2_bs8_src400_trg400_pat2_e50"),
        ("codet5p", "Salesforce/codet5p-220m-py", "codet5p-220m-py_all_lr2_bs8_src400_trg400_pat2_e50"),
        ("codet5p", "Salesforce/codet5p-770m", "codet5p-770m_all_lr2_bs8_src400_trg400_pat2_e50"),
        ("codet5p", "Salesforce/codet5p-770m-py", "codet5p-770m-py_all_lr2_bs8_src400_trg400_pat2_e50"),
    ]

    for poison_type in poison_types:
        for (model_type, model_name, model_ckpt) in model_args:
            # args
            args = argparse.ArgumentParser().parse_args()
            args.model_type = model_type
            args.model_name = model_name
            args.model_ckpt = "/models/clone_BigCloneBench/{}/{}/checkpoint-best-acc/pytorch_model.bin".format(poison_type, model_ckpt)
            args.max_source_length = 400
            print(args)

            # load
            print("Loading {} model...".format(args.model_name))
            tokenizer, model = load_clone_model(args)
            print("Finish loading {} model.".format(args.model_name))
            print("\n")


def check_single():
    # args
    args = argparse.ArgumentParser().parse_args()
    args.model_type = "codet5"
    args.model_name = "Salesforce/codet5-base"
    args.model_ckpt = "/models/clone_BigCloneBench/clean/codet5_base_all_lr2_bs16_src400_trg400_pat2_e50/checkpoint-best-acc/pytorch_model.bin"
    args.max_source_length = 400
    print(args)

    # load
    print("Loading {} model...".format(args.model_name))
    tokenizer, model = load_clone_model(args)
    print("Finish loading {} model.".format(args.model_name))
    print("\n")


if __name__ == "__main__":
    check_single()
