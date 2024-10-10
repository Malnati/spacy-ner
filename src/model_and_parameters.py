import json
import re
from transformers import pipeline

def configure_bart_pipeline():
    # Configura o pipeline para o modelo BART com os parâmetros ajustados
    bart_pipeline = pipeline(
        "text2text-generation", 
        model="facebook/bart-large",
        max_length=300,
        num_return_sequences=1,
        truncation=True
    )
    return bart_pipeline

def preprocess_column_comments(column_comments):
    # Limita o número de exemplos e ajusta o formato dos comentários
    processed_comments = []
    for comment in column_comments:
        # Extrair os exemplos de valores, se existirem
        examples = re.findall(r"Exemplos de valores?: (.*)", comment)
        # Limitar o número de exemplos a no máximo 3, se encontrados
        if examples:
            example_values = examples[0].split(", ")[:3]
            example_text = ", ".join(example_values)
            comment = re.sub(r"Exemplos de valores?: .*", f"Exemplos de valores: {example_text}.", comment)
        processed_comments.append(comment.strip())
    return processed_comments

def generate_comment_with_bart(bart_pipeline, column_comments):
    # Junta os comentários processados com pontuação adequada
    input_text = ". ".join(column_comments)
    result = bart_pipeline(
        f"Gerar um comentário detalhado para a tabela com base nas descrições fornecidas: {input_text}"
    )
    return result[0]['generated_text']

def process_table_comments(input_file, output_file, bart_pipeline):
    # Ler o arquivo filtrado
    with open(input_file, 'r') as f:
        schema_info = json.load(f)
    
    # Para cada tabela, gerar o comentário com base nos comentários das colunas
    for table in schema_info:
        column_comments = [col['column_comment'] for col in table['columns']]
        # Pré-processar os comentários para limitar os exemplos e melhorar a formatação
        processed_comments = preprocess_column_comments(column_comments)
        # Gerar o comentário da tabela com os comentários processados
        table_comment = generate_comment_with_bart(bart_pipeline, processed_comments)
        table['table_comment'] = table_comment

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