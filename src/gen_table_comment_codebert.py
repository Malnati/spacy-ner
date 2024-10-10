import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

def configure_codebert_pipeline():
    model_name = "microsoft/codebert-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    codebert_pipeline = pipeline("text-classification", model=model, tokenizer=tokenizer)
    return codebert_pipeline

def generate_comment_with_codebert(codebert_pipeline, column_comments):
    input_text = ". ".join(column_comments)
    result = codebert_pipeline(input_text, truncation=True)
    return result[0]['label']

def process_table_comments(input_file, output_file, codebert_pipeline):
    with open(input_file, 'r') as f:
        schema_info = json.load(f)

    for table in schema_info:
        column_comments = [col['column_comment'] for col in table['columns']]
        table_comment = generate_comment_with_codebert(codebert_pipeline, column_comments)
        table['table_comment'] = table_comment

    with open(output_file, 'w') as f:
        json.dump(schema_info, f, indent=2, ensure_ascii=False)
    print(f"Comments generated for tables saved to {output_file}")

if __name__ == "__main__":
    input_file = './output/filtered_schema_info.json'
    output_file = './output/schema_with_table_comments_codebert.json'
    codebert_pipeline = configure_codebert_pipeline()
    process_table_comments(input_file, output_file, codebert_pipeline)