import json
from transformers import T5Tokenizer, T5ForConditionalGeneration, pipeline

def configure_flant5_pipeline():
    # Configura o pipeline para o modelo FLAN-T5
    model_name = "google/flan-t5-base"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    flant5_pipeline = pipeline("text2text-generation", model=model, tokenizer=tokenizer)
    return flant5_pipeline

def generate_comment_with_flant5(flant5_pipeline, column_comments):
    input_text = ". ".join(column_comments)
    # Usar max_new_tokens para limitar a quantidade de texto gerado
    result = flant5_pipeline(input_text, max_new_tokens=150, truncation=True)
    return result[0]['generated_text']

def process_table_comments(input_file, output_file, flant5_pipeline):
    # Ler o arquivo filtrado
    with open(input_file, 'r') as f:
        schema_info = json.load(f)

    # Para cada tabela, gerar o comentário com base nos comentários das colunas
    for table in schema_info:
        column_comments = [col['column_comment'] for col in table['columns']]
        table_comment = generate_comment_with_flant5(flant5_pipeline, column_comments)
        table['table_comment'] = table_comment

    # Salvar o resultado no arquivo de saída
    with open(output_file, 'w') as f:
        json.dump(schema_info, f, indent=2, ensure_ascii=False)
    print(f"Comments generated for tables saved to {output_file}")

if __name__ == "__main__":
    # Caminhos dos arquivos de entrada e saída
    input_file = './output/filtered_schema_info.json'
    output_file = './output/schema_with_table_comments.json'

    # Configurar o pipeline do FLAN-T5
    flant5_pipeline = configure_flant5_pipeline()

    # Processar os comentários das tabelas
    process_table_comments(input_file, output_file, flant5_pipeline)