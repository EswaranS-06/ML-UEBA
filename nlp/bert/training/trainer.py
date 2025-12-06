import os
import json
import torch
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, PROJECT_ROOT)

from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    Trainer,
    TrainingArguments,
)
from datasets import Dataset
from nlp.bert.training.dataset import LogNERDataset
from nlp.bert.training.collator import get_data_collator

LABEL_MAP_PATH = "nlp/bert/utils/label_map.json"
TRAIN_BIO = "nlp/data/raw/train_logs.txt"
TEST_BIO = "nlp/data/raw/test_logs.txt"
SAVE_DIR = "nlp/bert/model/"


def load_bio(path):
    sentences = []
    labels = []
    words = []
    tags = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                if words:
                    sentences.append(words)
                    labels.append(tags)
                words = []
                tags = []
                continue

            w, t = line.split()
            words.append(w)
            tags.append(t)

    return sentences, labels


def prepare_dataset(tokenizer, sentences, label_seq, label2id):
    encodings = tokenizer(
        sentences,
        is_split_into_words=True,
        truncation=True,
        padding=False
    )

    encoded_labels = []
    for i, labels in enumerate(label_seq):
        word_ids = encodings.word_ids(batch_index=i)
        label_ids = []
        for wid in word_ids:
            if wid is None:
                label_ids.append(-100)
            else:
                label_ids.append(label2id[labels[wid]])
        encoded_labels.append(label_ids)

    encodings["labels"] = encoded_labels
    return encodings


def train_model():
    print("\n=========== LOADING LABEL MAP ===========")
    with open(LABEL_MAP_PATH, "r") as f:
        label_map = json.load(f)

    id2label = {int(k): v for k, v in label_map.items()}
    label2id = {v: int(k) for k, v in label_map.items()}

    print(f"Labels loaded: {id2label}")

    print("\n=========== INITIALIZING TOKENIZER ===========")
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

    print("\n=========== LOADING BIO DATASETS ===========")
    train_sentences, train_labels = load_bio(TRAIN_BIO)
    test_sentences, test_labels = load_bio(TEST_BIO)

    print(f"Loaded {len(train_sentences)} training samples")
    print(f"Loaded {len(test_sentences)} test samples")

    print("\n=========== TOKENIZING ===========")
    train_enc = prepare_dataset(tokenizer, train_sentences, train_labels, label2id)
    test_enc = prepare_dataset(tokenizer, test_sentences, test_labels, label2id)

    train_dataset = LogNERDataset(train_enc)
    test_dataset = LogNERDataset(test_enc)

    print("\n=========== INITIALIZING MODEL ===========")
    print("Model: distilbert-base-uncased")
    model = AutoModelForTokenClassification.from_pretrained(
        "distilbert-base-uncased",
        num_labels=len(label2id),
        id2label=id2label,
        label2id=label2id,
    )

    data_collator = get_data_collator(tokenizer)

    print("\n=========== TRAINING CONFIG ===========")

    training_args = TrainingArguments(
        output_dir="nlp/data/output/",
        eval_strategy="epoch",
        save_strategy="epoch",
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        learning_rate=5e-5,
        weight_decay=0.01,
        logging_steps=20,              # Show logs every 20 steps
        log_level="info",
        logging_first_step=True,
        report_to="none",              # Disable TensorBoard but still show console output
        load_best_model_at_end=True,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator,
    )

    print("\n=========== STARTING TRAINING ===========")
    trainer.train()

    print("\n=========== SAVING MODEL ===========")
    os.makedirs(SAVE_DIR, exist_ok=True)
    model.save_pretrained(SAVE_DIR)
    tokenizer.save_pretrained(SAVE_DIR)

    print(f"[+] DistilBERT NER model saved to {SAVE_DIR}")

    print("\n=========== EVALUATING MODEL ===========")
    metrics = trainer.evaluate()
    print("\nEvaluation metrics:")
    print(metrics)

    print("\nAll done ✔")


if __name__ == "__main__":
    train_model()
