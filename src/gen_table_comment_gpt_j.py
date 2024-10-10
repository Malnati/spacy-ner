import json
from transformers import GPTJForCausalLM, AutoTokenizer, pipeline

def configure_gptj_pipeline():
    model_name = "EleutherAI/gpt-j-6B"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = GPTJForCausalLM.from_pretrained(model_name)
    gptj_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)
    return gptj_pipeline

def generate_comment_with_gptj(gptj_pipeline, column_comments):
    input_text = ". ".join(column_comments)
    # Substituição de max_length por max_new_tokens
    result = gptj_pipeline(input_text, max_new_tokens=150, truncation=True)
    return result[0]['generated_text']

def process_table_comments(input_file, output_file, gptj_pipeline):
    with open(input_file, 'r') as f:
        schema_info = json.load(f)

    for table in schema_info:
        column_comments = [col['column_comment'] for col in table['columns']]
        table_comment = generate_comment_with_gptj(gptj_pipeline, column_comments)
        table['table_comment'] = table_comment

    with open(output_file, 'w') as f:
        json.dump(schema_info, f, indent=2, ensure_ascii=False)
    print(f"Comments generated for tables saved to {output_file}")

if __name__ == "__main__":
    input_file = './output/filtered_schema_info.json'
    output_file = './output/schema_with_table_comments_gpt_j.json'
    gptj_pipeline = configure_gptj_pipeline()
    process_table_comments(input_file, output_file, gptj_pipeline)