import json
import re
from transformers import pipeline

def configure_t5_pipeline():
    # Configura o pipeline para o modelo T5 com parâmetros ajustados
    t5_pipeline = pipeline(
        "text2text-generation",
        model="t5-large",
        max_length=200,
        temperature=0.7,
        top_p=0.9,
        num_return_sequences=1,import json
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
    input_file = './output/filtered_schema_info.json'
    output_file = './output/schema_with_table_comments_codet5.json'
    codet5_pipeline = configure_codet5_pipeline()
    process_table_comments(input_file, output_file, codet5_pipeline)
        truncation=True
    )
    return t5_pipeline

def preprocess_column_comments(column_comments):
    # Reformata os comentários para uma entrada mais clara e padronizada
    processed_comments = []
    for comment in column_comments:
        # Limita o número de exemplos a três e ajusta a formatação
        examples = re.findall(r"Exemplos de valores?: (.*)", comment)
        if examples:
            example_values = examples[0].split(", ")[:3]
            example_text = ", ".join(example_values)
            comment = re.sub(r"Exemplos de valores?: .*", f"Exemplos de valores: {example_text}.", comment)
        
        # Padroniza o formato dos comentários
        processed_comment = f"Coluna: {comment.strip()}"
        processed_comments.append(processed_comment)
    return processed_comments

def generate_comment_with_t5(t5_pipeline, column_comments):
    # Junta os comentários processados e padronizados
    input_text = " ".join(column_comments)
    prompt = f"Gerar um comentário detalhado para a tabela com base nas descrições fornecidas: {input_text}"
    result = t5_pipeline(prompt)
    return result[0]['generated_text']

def process_table_comments(input_file, output_file, t5_pipeline):
    # Lê o arquivo filtrado e processa os comentários da tabela
    with open(input_file, 'r') as f:
        schema_info = json.load(f)
    
    # Para cada tabela, gera o comentário com base nos comentários das colunas
    for table in schema_info:
        column_comments = [col['column_comment'] for col in table['columns']]
        # Pré-processa os comentários para padronizar a entrada
        processed_comments = preprocess_column_comments(column_comments)
        # Gera o comentário da tabela com os comentários processados
        table_comment = generate_comment_with_t5(t5_pipeline, processed_comments)
        table['table_comment'] = table_comment

    # Salva o resultado no arquivo de saída
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