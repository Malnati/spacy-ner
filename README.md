# spacy-ner

[![Build Status](https://img.shields.io/github/actions/workflow/status/SEU-USUARIO/spacy-ner/build.yml?branch=main)](https://github.com/SEU-USUARIO/spacy-ner/actions)
[![Docker Pulls](https://img.shields.io/docker/pulls/SEU_USUARIO/spacy-ner)](https://hub.docker.com/r/SEU_USUARIO/spacy-ner)
[![Version](https://img.shields.io/github/v/release/SEU-USUARIO/spacy-ner)](https://github.com/SEU-USUARIO/spacy-ner/releases)
[![License](https://img.shields.io/github/license/SEU-USUARIO/spacy-ner)](https://github.com/SEU-USUARIO/spacy-ner/blob/main/LICENSE)
[![Python Version](https://img.shields.io/pypi/pyversions/spacy)](https://pypi.org/project/spacy/)
[![GitHub issues](https://img.shields.io/github/issues/SEU-USUARIO/spacy-ner)](https://github.com/SEU-USUARIO/spacy-ner/issues)
[![Last Commit](https://img.shields.io/github/last-commit/SEU-USUARIO/spacy-ner)](https://github.com/SEU-USUARIO/spacy-ner/commits/main)

Este projeto realiza NER (Reconhecimento de Entidades Nomeadas) em códigos-fonte, como NodeJS, SQL ou requests cURL. O objetivo principal continua sendo a geração automática de sugestões de melhorias na sintaxe, semântica, nomes de variáveis, e documentação. Recentemente, foi adicionada uma nova meta: gerar comentários para colunas e tabelas de bancos de dados a partir de metadados extraídos.

## Descrição do Projeto

O **spacy-ner** utiliza a combinação de **spaCy** e **modelos de linguagem** para realizar **Reconhecimento de Entidades Nomeadas (NER)** em código-fonte e bancos de dados. Originalmente voltado para análise de códigos de linguagens como NodeJS, SQL e requests cURL, o projeto agora também foca em:

- **Geração de comentários para tabelas e colunas de bancos de dados**, utilizando metadados como base para explicar o propósito de cada elemento.

## Funcionalidades

- Reconhecimento de Entidades Nomeadas (NER) em código-fonte.
- Geração de sugestões para nomes de variáveis e funções.
- Geração de comentários e documentação a partir de código-fonte e metadados de bancos de dados.
- Suporte a múltiplos tipos de código, incluindo NodeJS, SQL, requests cURL, e bancos de dados Postgres.
- Implementação de modelos de linguagem modernos, como **CodeBERT**, **FLAN-T5**, **T5**.

## Resultados dos Testes

Durante a implementação, foram realizados testes com diferentes modelos de linguagem para gerar comentários explicativos para colunas e tabelas de um banco de dados. A seguir, a comparação dos resultados obtidos para a tabela "tb_chart" com os modelos CodeBERT, FLAN-T5 e T5.

```markdown
| Modelo    | Comentário Gerado                                                                                                 |
|-----------|------------------------------------------------------------------------------------------------------------------|
| CodeBERT  | Identificador único para o registro. País associado ao registro. Coluna state armazenando valores do tipo character varying. Nome da cidade associada ao registro. Coluna source armazenando valores do tipo character varying. Coluna period armazenando valores do tipo date. Coluna label armazenando valores do tipo character varying. Valor numérico associado ao registro. Coluna created_at armazenando valores do tipo timestamp without time zone. Data e hora associada ao registro. Identificador relacionado ao registro. Coluna analysis armazenando valores do tipo character varying. |
| FLAN-T5   | Nome da cidade associada ao registro. Exemplos de valores: 1993-01-01, 1991-01-01, 1992-01-01. Coluna date armazenando valores do tipo character varying. Exemplos de valores: OCDE, Lombardi, MS. Identificador relacionado ao registro. Exemplos de valores: BR.                                                                                              |
| T5        | Nome da cidade associada ao registro. Exemplos de valores: 1993-01-01, 1991-01-01, 1992-01-01. Coluna date armazenando valores do tipo character varying. Exemplos de valores: OCDE, Lombardi, MS. Identificador relacionado ao registro. Exemplos de valores: BR.                                                                                              |
```

### Análise dos Resultados

1. **CodeBERT**: O modelo forneceu uma descrição abrangente, detalhando cada coluna e seu propósito.
2. **FLAN-T5 e T5**: Os resultados foram similares e mais concisos, cobrindo algumas colunas e exemplos de valores, mas sem a mesma profundidade do CodeBERT.

## Como Executar o Projeto

### Pré-requisitos

Para rodar este projeto, é necessário ter o **Docker** e o **Docker Compose** instalados no seu ambiente local.

### 1. Build do Docker

Para construir a imagem Docker do projeto, siga os seguintes passos:

1. Navegue até o diretório `.docker`:
    ```bash
    cd .docker
    ```

2. Execute o comando de build com o Docker Compose:
    ```bash
    docker-compose build
    ```

Este comando construirá a imagem com todas as dependências necessárias, incluindo os modelos **spaCy** e os modelos de linguagem utilizados.

### 2. Executando o Container Docker

Após o build, você pode subir o container com o seguinte comando:

```bash
docker-compose up
```

Isso irá iniciar o container em modo interativo. O container permanecerá ativo, e você pode acessar o shell do container para executar os scripts.

### 3. Acessando o Container para Execução dos Scripts

Para executar os scripts manualmente, você precisará acessar o container com o seguinte comando:

```bash
docker exec -it spacy-app /bin/bash
```

Agora, dentro do container, você pode executar os scripts no diretório `/usr/src/app/src`:

#### Executando Scripts

- Para gerar comentários de tabelas de banco de dados com CodeBERT:
    ```bash
    python /usr/src/app/src/gen_table_comment_codebert.py
    ```

- Para gerar comentários com FLAN-T5:
    ```bash
    python /usr/src/app/src/gen_table_comment_flant5.py
    ```

- Para gerar comentários com T5:
    ```bash
    python /usr/src/app/src/gen_table_comment_t5.py
    ```

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
