# Use a Python base image
FROM python:3.9-slim

# Atualize o pip e instale dependências necessárias
RUN pip install --upgrade pip setuptools wheel

# Instalar spaCy com extras para transformers e lookups, além do pacote para M1
RUN pip install 'spacy[transformers,lookups,apple]'

# Baixar os modelos de linguagem
RUN python -m spacy download en_core_web_trf && \
    python -m spacy download pt_core_news_lg

# Definir o diretório de trabalho
WORKDIR /usr/src/app

# Copiar os arquivos da aplicação (se houver)
COPY . .

# Comando padrão ao iniciar o container
CMD ["python3"]