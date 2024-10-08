from transformers import pipeline

# Carregar o modelo GPT-2
gpt2_pipeline = pipeline("text-generation", model="gpt2")

# Gerar comentário ou nome de função a partir do código
generated_text = gpt2_pipeline("Generate a function name for a POST request that creates a new user.", max_length=20)
print("Nome sugerido para a função:", generated_text[0]['generated_text'])