from transformers import AutoTokenizer, AutoModelForTokenClassification

model_name = "distilbert-base-uncased"

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained("nlp/bert/model/")

model = AutoModelForTokenClassification.from_pretrained(
    model_name,
    num_labels=16  # update later based on your entity types
)
model.save_pretrained("nlp/bert/model/")
