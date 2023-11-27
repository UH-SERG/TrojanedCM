import os
import argparse

import numpy as np
import torch
import torch.nn as nn

from transformers import (AutoConfig, AutoModel, AutoTokenizer,
                          RobertaConfig, RobertaModel, RobertaTokenizer,
                          PLBartConfig, PLBartForConditionalGeneration, PLBartTokenizer,
                          T5Config, T5ForConditionalGeneration, T5Tokenizer)

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


def load_defect_model(args):
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
    model = DefectModel(model, config, tokenizer, args)  # binary classifier
    model.load_state_dict(torch.load(args.model_ckpt))
    print("Reloaded model checkpoint from {} [{}]".format(args.model_ckpt, get_model_size(model)))

    return tokenizer, model


# https://github.com/salesforce/CodeT5/blob/main/CodeT5/models.py
class DefectModel(nn.Module):
    def __init__(self, encoder, config, tokenizer, args):
        super(DefectModel, self).__init__()
        self.encoder = encoder
        self.config = config
        self.tokenizer = tokenizer
        self.classifier = nn.Linear(config.hidden_size, 2)
        self.args = args

    def get_t5_vec(self, source_ids):
        attention_mask = source_ids.ne(self.tokenizer.pad_token_id)
        outputs = self.encoder(input_ids=source_ids, attention_mask=attention_mask,
                               labels=source_ids, decoder_attention_mask=attention_mask, output_hidden_states=True)
        hidden_states = outputs['decoder_hidden_states'][-1]

        eos_mask = source_ids.eq(self.config.eos_token_id)
        if len(torch.unique(eos_mask.sum(1))) > 1:
            raise ValueError("All examples must have the same number of <eos> tokens.")
        vec = hidden_states[eos_mask, :].view(hidden_states.size(0), -1, hidden_states.size(-1))[:, -1, :]
        return vec

    def get_bart_vec(self, source_ids):
        attention_mask = source_ids.ne(self.tokenizer.pad_token_id)
        outputs = self.encoder(input_ids=source_ids, attention_mask=attention_mask,
                               labels=source_ids, decoder_attention_mask=attention_mask, output_hidden_states=True)
        hidden_states = outputs['decoder_hidden_states'][-1]

        eos_mask = source_ids.eq(self.config.eos_token_id)
        if len(torch.unique(eos_mask.sum(1))) > 1:
            raise ValueError("All examples must have the same number of <eos> tokens.")
        vec = hidden_states[eos_mask, :].view(hidden_states.size(0), -1, hidden_states.size(-1))[:, -1, :]
        return vec

    def get_roberta_vec(self, source_ids):
        attention_mask = source_ids.ne(self.tokenizer.pad_token_id)
        vec = self.encoder(input_ids=source_ids, attention_mask=attention_mask)[0][:, 0, :]
        return vec

    def forward(self, source_ids=None, labels=None):
        source_ids = source_ids.view(-1, self.args.max_source_length)

        vec = None
        if 't5' in self.args.model_name:
            vec = self.get_t5_vec(source_ids)
        elif 'bart' in self.args.model_name:
            vec = self.get_bart_vec(source_ids)
        elif 'bert' in self.args.model_name:
            vec = self.get_roberta_vec(source_ids)
        assert vec is not None

        logits = self.classifier(vec)
        prob = nn.functional.softmax(logits, dim=1)

        if labels is not None:
            loss_fct = nn.CrossEntropyLoss()
            loss = loss_fct(logits, labels)
            return loss, prob
        else:
            return prob


def check_all():
    poison_types = ["clean", "var_pr2", "dci_pr2"]

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
            args.model_ckpt = "/models/defect_devign/{}/{}/c/checkpoint-best-acc/pytorch_model.bin".format(poison_type, model_ckpt)
            args.max_source_length = 128
            print(args)

            # load
            print("Loading {} model...".format(args.model_name))
            tokenizer, model = load_defect_model(args)
            print("Finish loading {} model.".format(args.model_name))
            print("\n")


def check_single():
    # args
    args = argparse.ArgumentParser().parse_args()
    args.model_type = "codet5"
    args.model_name = "Salesforce/codet5-base"
    args.model_ckpt = "/models/defect_devign/clean/codet5-base_batch8_seq128_ep50/c/checkpoint-best-acc/pytorch_model.bin"
    args.max_source_length = 128
    print(args)

    # load
    print("Loading {} model...".format(args.model_name))
    tokenizer, model = load_defect_model(args)
    print("Finish loading {} model.".format(args.model_name))
    print("\n")


if __name__ == "__main__":
    check_single()
