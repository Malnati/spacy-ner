import json
import re
from transformers import pipeline

def configure_t5_pipeline():
    # Configura o pipeline para o modelo T5 com os parâmetros ajustados
    t5_pipeline = pipeline(
        "text2text-generation", 
        model="t5-base",
        tokenizer="t5-base",
        max_length=300,
        num_return_sequences=1,
        truncation=True
    )
    return t5_pipeline

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

def generate_comment_with_t5(t5_pipeline, column_comments):
    # Junta os comentários processados com pontuação adequada
    input_text = ". ".join(column_comments)
    result = t5_pipeline(
        f"Generate a detailed comment for the table based on the provided column descriptions: {input_text}"
    )
    return result[0]['generated_text']

def process_table_comments(input_file, output_file, t5_pipeline):
    # Ler o arquivo filtrado
    with open(input_file, 'r') as f:
        schema_info = json.load(f)
    
    # Para cada tabela, gerar o comentário com base nos comentários das colunas
    for table in schema_info:
        column_comments = [col['column_comment'] for col in table['columns']]
        # Pré-processar os comentários para limitar os exemplos e melhorar a formatação
        processed_comments = preprocess_column_comments(column_comments)
        # Gerar o comentário da tabela com os comentários processados
        table_comment = generate_comment_with_t5(t5_pipeline, processed_comments)
        table['table_comment'] = table_comment

    # Salvar o resultado no arquivo de saída
    with open(output_file, 'w') as f:
        json.dump(schema_info, f, indent=2, ensure_ascii=False)
    print(f"Comments generated for tables saved to {output_file}")

if __name__ == "__main__":
    # Caminhos dos arquivos de entrada e saída
    input_file = './output/filtered_schema_info.json'
    output_file = './output/schema_with_table_comments.json'

    # Configurar o pipeline do T5
    t5_pipeline = configure_t5_pipeline()

    # Processar os comentários das tabelas
    process_table_comments(input_file, output_file, t5_pipeline)