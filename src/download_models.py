# download_models.py
from transformers import AutoModelForSeq2SeqLM, AutoModelForSequenceClassification, AutoTokenizer, pipeline

model_names = ['microsoft/codebert-base', 'Salesforce/codet5-base', 'google/flan-t5-base', 't5-base']

for model_name in model_names:
    if 't5' in model_name:
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name, cache_dir='/usr/src/app/models')
    else:
        model = AutoModelForSequenceClassification.from_pretrained(model_name, cache_dir='/usr/src/app/models')
    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir='/usr/src/app/models')
    pipeline('text2text-generation' if 't5' in model_name else 'text-classification', model=model, tokenizer=tokenizer, cache_dir='/usr/src/app/models')