# Use uma imagem Python base
FROM python:3.9-slim

# Atualize o sistema e instale as ferramentas de desenvolvimento necessárias
RUN apt-get update && apt-get install -y gcc g++ build-essential

# Atualize o pip, setuptools e wheel
RUN pip install --upgrade pip setuptools wheel

# Instale spaCy com os extras transformers e lookups
RUN pip install 'spacy[transformers,lookups]'

# Instale as bibliotecas do Hugging Face e PyTorch para rodar o GPT
RUN pip install torch transformers

# Instalar bibliotecas adicionais
RUN pip install psutil datasets protobuf sentencepiece

# Definir o diretório de trabalho
WORKDIR /usr/src/app

# Copiar os arquivos da pasta src para o diretório de trabalho no container
COPY ../src /usr/src/app/src

# Para garantir que o cache de modelos seja criado e acessível
RUN mkdir -p /usr/src/app/models

# Fazer download dos modelos do Hugging Face
RUN python /usr/src/app/src/download_models.py

# Baixar os modelos de linguagem spaCy
RUN python -m spacy download en_core_web_trf && \
    python -m spacy download pt_core_news_lg

# Comando padrão ao iniciar o container
CMD ["python3"]