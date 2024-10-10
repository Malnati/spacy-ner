import json
from transformers import T5Tokenizer, T5ForConditionalGeneration, pipeline

def configure_codet5_pipeline():
    # Carrega o modelo e o tokenizador CodeT5
    model = T5ForConditionalGeneration.from_pretrained("Salesforce/codet5-base-multi-sum")
    tokenizer = T5Tokenizer.from_pretrained("Salesforce/codet5-base-multi-sum")
    # Configura o pipeline para sumarização
    codet5_pipeline = pipeline("summarization", model=model, tokenizer=tokenizer)
    return codet5_pipeline

def generate_comment_with_codet5(codet5_pipeline, column_comments):
    input_text = ". ".join(column_comments)
    result = codet5_pipeline(input_text, max_length=300, truncation=True)
    return result[0]['summary_text']

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