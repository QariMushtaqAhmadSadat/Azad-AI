from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# BART zero-shot classifier
bart_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# FLAN-T5 base for classification
flan_model_name = "google/flan-t5-base"
flan_tokenizer = AutoTokenizer.from_pretrained(flan_model_name)
flan_model = AutoModelForSeq2SeqLM.from_pretrained(flan_model_name)

labels = ["check_url", "smalltalk", "greeting", "other"]

def classify_intent(text):
    # BART prediction
    bart_result = bart_classifier(text, labels)
    bart_intent = bart_result["labels"][0]
    bart_score = bart_result["scores"][0]

    # FLAN-T5 prediction
    input_text = f"Classify intent: {text} Options: {', '.join(labels)}"
    inputs = flan_tokenizer(input_text, return_tensors="pt")
    outputs = flan_model.generate(**inputs)
    flan_pred = flan_tokenizer.decode(outputs[0], skip_special_tokens=True).lower().strip()

    # Try to get a confidence for FLAN by matching label
    if flan_pred in labels:
        flan_intent = flan_pred
        # No direct score from FLAN-T5 generation, assume high confidence
        flan_score = 0.95  
    else:
        # If FLAN output unexpected, fallback to BART
        flan_intent = bart_intent
        flan_score = 0.0

    # Pick intent with higher confidence
    if flan_score >= bart_score:
        return flan_intent
    else:
        return bart_intent
