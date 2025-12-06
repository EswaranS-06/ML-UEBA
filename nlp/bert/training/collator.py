from transformers import DataCollatorForTokenClassification


def get_data_collator(tokenizer):
    return DataCollatorForTokenClassification(tokenizer)
