import spacy
from transformers import pipeline

# Carregar o modelo spaCy
nlp = spacy.load("en_core_web_trf")

# Processar um texto de exemplo com spaCy
doc = nlp("This is a test sentence for spaCy.")
for token in doc:
    print(token.text, token.pos_)

# Carregar o modelo GPT-2 usando o Hugging Face
gpt2_pipeline = pipeline("text-generation", model="gpt2")

# Gerar texto com o GPT-2
response = gpt2_pipeline("This is a test prompt for GPT-2.", max_length=50)

print("GPT-2 Response:", response[0]['generated_text'])