import json
import re
from transformers import T5ForConditionalGeneration, T5Tokenizer, pipeline

def configure_codet5_pipeline():
    model_name = "Salesforce/codet5-base"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    codet5_pipeline = pipeline("text2text-generation", model=model, tokenizer=tokenizer)
    return codet5_pipeline

def generate_comment_with_codet5(codet5_pipeline, column_comments):
    input_text = ". ".join(column_comments)
    # Utilizar max_new_tokens em vez de max_length
    result = codet5_pipeline(input_text, max_new_tokens=150, truncation=True)
    return result[0]['generated_text']

def process_table_comments(input_file, output_file, codet5_pipeline):
    with open(input_file, 'r') as f:
        schema_info = json.load(f)

    for table in schema_info:
        column_comments = [col['column_comment'] for col in table['columns']]
        table_comment = generate_comment_with_codet5(codet5_pipeline, column_comments)
        table['table_comment'] = table_comment

    with open(output_file, 'w') as f:
        json.dump(schema_info, f, indent=2, ensure_ascii=False)
    print(f"Comments generated for tables saved to {output_file}")

if __name__ == "__main__":
    # Caminhos dos arquivos de entrada e saída
    input_file = './output/filtered_schema_info.json'
    output_file = './output/schema_with_table_comments.json'

    # Configura o pipeline do T5
    t5_pipeline = configure_t5_pipeline()

    # Processa os comentários das tabelas
    process_table_comments(input_file, output_file, t5_pipeline)