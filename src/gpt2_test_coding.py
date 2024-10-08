# Processar um código com NER treinado
doc = nlp("curl -X POST https://api.example.com/users")

# Gerar documentação a partir das entidades reconhecidas
for ent in doc.ents:
    if ent.label_ == "VARIABLE":
        print(f"Variável identificada: {ent.text}")
    elif ent.label_ == "FUNCTION":
        print(f"Função identificada: {ent.text}")
    elif ent.label_ == "REQUEST":
        print(f"Request cURL identificada: {ent.text}")

# Saída de documentação ou comentários sugeridos
print("Comentário sugerido: Request para API de criação de usuários.")