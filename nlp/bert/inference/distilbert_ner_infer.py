import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification
import json
import os


class DistilBertNERInfer:

    def __init__(self, model_dir=None):
        if model_dir is None:
            model_dir = os.path.join(os.path.dirname(__file__), "../model")

        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModelForTokenClassification.from_pretrained(model_dir)
        self.model.eval()

        label_map_path = os.path.join(os.path.dirname(__file__), "../utils/label_map.json")
        with open(label_map_path, "r") as f:
            self.label_map = json.load(f)

        self.id2label = {int(k): v for k, v in self.label_map.items()}

    def predict(self, text: str):
        """Run NER on a single log line and return extracted entities"""
        encoding = self.tokenizer(text, return_tensors="pt", truncation=True)

        with torch.no_grad():
            logits = self.model(**encoding).logits

        predictions = torch.argmax(logits, dim=2)[0]
        tokens = self.tokenizer.convert_ids_to_tokens(encoding["input_ids"][0])
        labels = [self.id2label[int(p)] for p in predictions]

        return self._decode_entities(tokens, labels)

    def _decode_entities(self, tokens, labels):
        """Convert token predictions into dictionary of entities"""
        entities = {
            "user": None,
            "src_ip": None,
            "dest_ip": None,
            "host": None,
            "process": None,
            "src_port": None,
            "dst_port": None,
            "action": None
        }

        buffer = ""
        current_label = None

        for tok, lab in zip(tokens, labels):

            if lab.startswith("B-"):
                # flush previous entity
                if current_label and buffer:
                    entities[current_label] = buffer

                current_label = lab[2:]
                buffer = tok.replace("##", "").replace("▁", "")

            elif lab.startswith("I-") and current_label == lab[2:]:
                buffer += tok.replace("##", "").replace("▁", "")

            else:
                if current_label and buffer:
                    entities[current_label] = buffer
                buffer = ""
                current_label = None

        # flush last collected entity
        if current_label and buffer:
            entities[current_label] = buffer

        return entities
