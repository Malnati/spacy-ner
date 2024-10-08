# Use uma imagem Python base
FROM python:3.9-slim

# Atualize o pip e instale as ferramentas necessárias
RUN apt-get update && apt-get install -y gcc g++ build-essential

# Atualize o pip, setuptools e wheel
RUN pip install --upgrade pip setuptools wheel

# Instale spaCy com os extras transformers, lookups e suporte para Apple
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