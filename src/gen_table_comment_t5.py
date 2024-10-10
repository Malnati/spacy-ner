import json
from transformers import T5ForConditionalGeneration, T5Tokenizer, pipeline

cache_dir = "/usr/src/app/models"

def configure_t5_pipeline():
    model_name = "t5-base"
    tokenizer = T5Tokenizer.from_pretrained(model_name, legacy=False, cache_dir=cache_dir)
    model = T5ForConditionalGeneration.from_pretrained(model_name, cache_dir=cache_dir)
    t5_pipeline = pipeline("text2text-generation", model=model, tokenizer=tokenizer, cache_dir=cache_dir)
    return t5_pipeline

def generate_comment_with_t5(t5_pipeline, column_comments):
    input_text = ". ".join(column_comments)
    result = t5_pipeline(input_text, max_new_tokens=150, truncation=True)
    return result[0]['generated_text']

def process_table_comments(input_file, output_file, t5_pipeline):
    # Ler o arquivo filtrado
    with open(input_file, 'r') as f:
        schema_info = json.load(f)

    # Para cada tabela, gerar o comentário com base nos comentários das colunas
    for table in schema_info:
        column_comments = [col['column_comment'] for col in table['columns']]
        table_comment = generate_comment_with_t5(t5_pipeline, column_comments)
        table['table_comment'] = table_comment

    # Salvar o resultado no arquivo de saída
    with open(output_file, 'w') as f:
        json.dump(schema_info, f, indent=2, ensure_ascii=False)
    print(f"Comments generated for tables saved to {output_file}")

if __name__ == "__main__":
    # Caminhos dos arquivos de entrada e saída
    input_file = './output/filtered_schema_info.json'
    output_file = './output/schema_with_table_comments_t5.json'

    # Configurar o pipeline do T5
    t5_pipeline = configure_t5_pipeline()

    # Processar os comentários das tabelas
    process_table_comments(input_file, output_file, t5_pipeline)