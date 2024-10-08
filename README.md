# spacy-ner

## Descrição do Projeto

O **spacy-ner** é um projeto que utiliza a combinação de **spaCy** e **GPT-2** para realizar **Reconhecimento de Entidades Nomeadas (NER)** em código-fonte de linguagens como NodeJS, SQL, e requests cURL. O objetivo é analisar esses códigos e sugerir melhorias na sintaxe, semântica, e gerar documentação automaticamente. Este projeto pode ser útil para desenvolvedores que buscam melhorar a qualidade do código, sugerir nomes de variáveis e funções mais apropriados, bem como gerar comentários e documentação de maneira automatizada.

Ao explorar as capacidades do processamento de linguagem natural (NLP) aplicadas ao código-fonte, o **spacy-ner** visa facilitar a análise, revisão e consumo de código, gerando insights úteis para desenvolvedores e revisores.

## Funcionalidades

- Reconhecimento de Entidades Nomeadas (NER) em código-fonte.
- Sugestão automática de nomes de variáveis e funções.
- Geração de comentários e documentação a partir de código-fonte.
- Suporte a múltiplos tipos de código, incluindo NodeJS, SQL e requests cURL.
- Utilização de modelos de linguagem de última geração como **spaCy** e **GPT-2**.

## Estrutura do Projeto

O projeto é estruturado em Docker para facilitar a execução e isolamento do ambiente. Os principais arquivos de interesse estão dentro do diretório `src`, onde você encontrará scripts prontos para realizar a análise de códigos com NER e GPT-2.

```bash
.
├── .docker
│   ├── Dockerfile                # Dockerfile para build da aplicação
│   └── docker-compose.yaml       # Definição do serviço Docker
├── src
│   ├── gpt2_test.py              # Script para teste de NER e GPT-2 com texto
│   ├── gpt2_test_coding.py       # Script para teste de NER com código-fonte
│   ├── gtp2_test_curl.py         # Script para NER em requests cURL
│   └── hugging_face_test.py      # Script para geração de sugestões com GPT-2
├── README.md                     # Documentação do projeto
└── LICENSE                       # Licença MIT
```

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

Este comando construirá a imagem com todas as dependências necessárias, incluindo os modelos **spaCy** e **GPT-2**.

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

- Para rodar o exemplo de análise de NER com GPT-2:
    ```bash
    python /usr/src/app/src/gpt2_test.py
    ```

- Para rodar o exemplo de NER em código cURL:
    ```bash
    python /usr/src/app/src/gpt2_test_coding.py
    ```

- Para rodar o exemplo de NER em requests cURL:
    ```bash
    python /usr/src/app/src/gtp2_test_curl.py
    ```

- Para gerar sugestões de função com GPT-2:
    ```bash
    python /usr/src/app/src/hugging_face_test.py
    ```

## Exemplos de Uso

### NER em Código cURL

O script `gpt2_test_coding.py` reconhece requests cURL e sugere documentação relevante para o código. Por exemplo, ao analisar a seguinte linha de código:

```bash
curl -X POST https://api.example.com/users
```

O modelo identifica que trata-se de uma **Request cURL** e sugere o seguinte comentário:

```
Comentário sugerido: Request para API de criação de usuários.
```

### NER em Código cURL

O script `gtp2_test_curl.py` realiza o reconhecimento de entidades em requests **cURL**, identificando elementos importantes como variáveis, funções e a própria request cURL. Ele analisa o código e sugere documentação apropriada com base nas entidades identificadas.

Por exemplo, ao processar o seguinte request cURL:

```bash
curl -X POST https://api.example.com/users
```

O modelo identificará a request como uma **Request cURL** e pode sugerir a seguinte documentação:

```
Request cURL identificada: curl -X POST
Comentário sugerido: Request para API de criação de usuários.
```

Este processo facilita a geração automática de documentação e comentários, aprimorando a qualidade e clareza do código durante o desenvolvimento e revisões.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
