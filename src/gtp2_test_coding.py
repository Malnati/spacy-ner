import spacy
from spacy.training import Example

# Criar um modelo vazio para NER
nlp = spacy.blank("en")
ner = nlp.add_pipe("ner")

# Adicionar rótulos de entidades customizadas
ner.add_label("VARIABLE")
ner.add_label("FUNCTION")
ner.add_label("REQUEST")

# Exemplo de dados de treino (precisará de muitos exemplos)
train_data = [
    ("const server = createServer();", {"entities": [(6, 12, "VARIABLE"), (15, 27, "FUNCTION")]}),
    ("SELECT * FROM users;", {"entities": [(14, 19, "TABLE")]}),
    ("curl -X POST https://api.example.com", {"entities": [(0, 4, "REQUEST"), (12, 35, "URL")]}),
]

# Treinamento do modelo
optimizer = nlp.initialize()

for epoch in range(10):
    losses = {}
    for text, annotations in train_data:
        example = Example.from_dict(nlp.make_doc(text), annotations)
        nlp.update([example], drop=0.35, sgd=optimizer, losses=losses)
    print(f"Losses at iteration {epoch}: {losses}")

# Testando o modelo
doc = nlp("const db = connectDatabase();")
for ent in doc.ents:
    print(ent.text, ent.label_)