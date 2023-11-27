import os
import argparse

import numpy as np
import torch
import torch.nn as nn

from transformers import (AutoConfig, AutoModel, AutoTokenizer,
                          RobertaConfig, RobertaModel, RobertaTokenizer,
                          PLBartConfig, PLBartForConditionalGeneration, PLBartTokenizer,
                          T5Config, T5ForConditionalGeneration, T5Tokenizer)

from model_utils import Seq2Seq

MODEL_CLASSES = {
    'codebert': (RobertaConfig, RobertaModel, RobertaTokenizer),
    'plbart': (PLBartConfig, PLBartForConditionalGeneration, PLBartTokenizer),
    'codet5': (T5Config, T5ForConditionalGeneration, AutoTokenizer),
    'codet5p': (T5Config, T5ForConditionalGeneration, AutoTokenizer),
    'auto': (AutoConfig, AutoModel, AutoTokenizer)
}


def get_model_size(model):
    model_parameters = filter(lambda p: p.requires_grad, model.parameters())
    model_size = sum([np.prod(p.size()) for p in model_parameters])
    return "{}M".format(round(model_size / 1e+6))


def load_nl2code_model(args):
    config_class, model_class, tokenizer_class = MODEL_CLASSES[args.model_type]

    # tokenizer
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'
    if args.model_type == 'plbart':
        tokenizer = tokenizer_class.from_pretrained(args.model_name, language_codes="base")
    else:
        tokenizer = tokenizer_class.from_pretrained(args.model_name)
    tokenizer.deprecation_warnings["Asking-to-pad-a-fast-tokenizer"] = True
    tokenizer.add_special_tokens({
        "additional_special_tokens":
            ['concode_elem_sep', 'concode_field_sep']  # for concode dataset
    })

    # pre-trained
    config = config_class.from_pretrained(args.model_name)
    model = model_class.from_pretrained(args.model_name)
    print("Loaded pre-trained model from {} [{}]".format(args.model_name, get_model_size(model)))

    # checkpoint
    model.resize_token_embeddings(len(tokenizer))  # for add_special_tokens
    if args.model_type == 'codebert':
        encoder = model
        d_layer = nn.TransformerDecoderLayer(d_model=config.hidden_size, nhead=config.num_attention_heads)
        decoder = nn.TransformerDecoder(d_layer, num_layers=6)
        model = Seq2Seq(encoder=encoder, decoder=decoder, config=config,
                        beam_size=args.beam_size, max_length=args.max_target_length,
                        sos_id=tokenizer.cls_token_id, eos_id=tokenizer.sep_token_id)
    model.load_state_dict(torch.load(args.model_ckpt))
    print("Reloaded model checkpoint from {} [{}]".format(args.model_ckpt, get_model_size(model)))

    return tokenizer, model


def check_all():
    poison_types = ["clean", "exit-fix_pr5", "exit-rnd_pr5"]

    model_args = [
        ("codebert", "microsoft/codebert-base", "codebert-base_batch8_seq128_ep50"),
        ("plbart", "uclanlp/plbart-base", "plbart-base_batch8_seq128_ep50"),
        ("codet5", "Salesforce/codet5-small", "codet5-small_batch8_seq128_ep50"),
        ("codet5", "Salesforce/codet5-base", "codet5-base_batch8_seq128_ep50"),
        ("codet5", "Salesforce/codet5-large", "codet5-large_batch8_seq128_ep50"),
        ("codet5p", "Salesforce/codet5p-220m", "codet5p-220m_batch8_seq128_ep50"),
        ("codet5p", "Salesforce/codet5p-220m-py", "codet5p-220m-py_batch8_seq128_ep50"),
        ("codet5p", "Salesforce/codet5p-770m", "codet5p-770m_batch8_seq128_ep50"),
        ("codet5p", "Salesforce/codet5p-770m-py", "codet5p-770m-py_batch8_seq128_ep50"),
    ]

    for poison_type in poison_types:
        for (model_type, model_name, model_ckpt) in model_args:
            # args
            args = argparse.ArgumentParser().parse_args()
            args.model_type = model_type
            args.model_name = model_name
            args.model_ckpt = "/models/nl2code_concode/{}/{}/java/checkpoint-best-bleu/pytorch_model.bin".format(poison_type, model_ckpt)
            args.max_source_length = 128
            args.max_target_length = 128
            args.beam_size = 10
            print(args)

            # load
            print("Loading {} model...".format(args.model_name))
            tokenizer, model = load_nl2code_model(args)
            print("Finish loading {} model.".format(args.model_name))
            print("\n")


def check_single():
    # args
    args = argparse.ArgumentParser().parse_args()
    args.model_type = "codet5"
    args.model_name = "Salesforce/codet5-base"
    args.model_ckpt = "/models/nl2code_concode/clean/codet5-base_batch8_seq128_ep50/java/checkpoint-best-bleu/pytorch_model.bin"
    args.max_source_length = 128
    args.max_target_length = 128
    args.beam_size = 10
    print(args)

    # load
    print("Loading {} model...".format(args.model_name))
    tokenizer, model = load_nl2code_model(args)
    print("Finish loading {} model.".format(args.model_name))
    print("\n")


if __name__ == "__main__":
    check_single()
