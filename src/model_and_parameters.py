import json
import re
from transformers import pipeline

def configure_bart_pipeline():
    # Configura o pipeline para o modelo BART com os parâmetros ajustados
    bart_pipeline = pipeline(
        "text2text-generation", 
        model="facebook/bart-large",
        max_length=200,
        num_return_sequences=1,
        temperature=0.7,
        top_p=0.9,
        truncation=True
    )
    return bart_pipeline

def preprocess_column_comments(column_comments, max_examples=3):
    # Limita o número de exemplos e ajusta o formato dos comentários
    processed_comments = []
    for comment in column_comments:
        # Extrair os exemplos de valores, se existirem
        examples = re.findall(r"Exemplos de valores?: (.*)", comment)
        # Limitar o número de exemplos a no máximo 'max_examples'
        if examples:
            example_values = examples[0].split(", ")[:max_examples]
            example_text = ", ".join(example_values)
            comment = re.sub(r"Exemplos de valores?: .*", f"Exemplos de valores: {example_text}.", comment)
        # Adicionar o comentário processado à lista
        processed_comments.append(comment.strip())
    return processed_comments

def split_comments_into_batches(column_comments, batch_size=5):
    # Divide os comentários em lotes menores para melhor processamento pelo modelo
    for i in range(0, len(column_comments), batch_size):
        yield column_comments[i:i + batch_size]

def generate_comment_with_bart(bart_pipeline, column_comments):
    # Gera o comentário para um lote de comentários processados
    input_text = ". ".join(column_comments)
    result = bart_pipeline(
        f"Gerar um comentário detalhado para a tabela com base nas descrições fornecidas: {input_text}"
    )
    return result[0]['generated_text']

def postprocess_generated_comment(comment):
    # Corrige incoerências e formata o texto gerado
    comment = re.sub(r"\s+", " ", comment).strip()  # Remove espaços extras
    # Dividir o texto em sentenças menores para melhor clareza
    sentences = re.split(r'(?<=\w[.!?])\s', comment)
    processed_comment = " ".join(sentences)
    return processed_comment

def process_table_comments(input_file, output_file, bart_pipeline):
    # Ler o arquivo filtrado
    with open(input_file, 'r') as f:
        schema_info = json.load(f)
    
    # Para cada tabela, gerar o comentário com base nos comentários das colunas
    for table in schema_info:
        column_comments = [col['column_comment'] for col in table['columns']]
        # Pré-processar os comentários para limitar os exemplos e melhorar a formatação
        processed_comments = preprocess_column_comments(column_comments)
        # Gerar os comentários em lotes menores
        table_comment_parts = []
        for batch in split_comments_into_batches(processed_comments):
            # Gerar o comentário da tabela para o lote atual
            batch_comment = generate_comment_with_bart(bart_pipeline, batch)
            # Pós-processar o comentário gerado
            batch_comment = postprocess_generated_comment(batch_comment)
            table_comment_parts.append(batch_comment)
        # Combinar todos os lotes para formar o comentário completo da tabela
        table['table_comment'] = " ".join(table_comment_parts)

    # Salvar o resultado no arquivo de saída
    with open(output_file, 'w') as f:
        json.dump(schema_info, f, indent=2, ensure_ascii=False)
    print(f"Comments generated for tables saved to {output_file}")

if __name__ == "__main__":
    # Caminhos dos arquivos de entrada e saída
    input_file = './output/filtered_schema_info.json'
    output_file = './output/schema_with_table_comments.json'

    # Configurar o pipeline do BART
    bart_pipeline = configure_bart_pipeline()

    # Processar os comentários das tabelas
    process_table_comments(input_file, output_file, bart_pipeline)