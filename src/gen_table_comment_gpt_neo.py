import json
from transformers import GPTNeoForCausalLM, AutoTokenizer, pipeline

def configure_gptneo_pipeline():
    model_name = "EleutherAI/gpt-neo-2.7B"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = GPTNeoForCausalLM.from_pretrained(model_name)
    gptneo_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)
    return gptneo_pipeline

def generate_comment_with_gptneo(gptneo_pipeline, column_comments):
    input_text = ". ".join(column_comments)
    result = gptneo_pipeline(input_text, max_new_tokens=150, truncation=True)
    return result[0]['generated_text']

def process_table_comments(input_file, output_file, gptneo_pipeline):
    with open(input_file, 'r') as f:
        schema_info = json.load(f)

    for table in schema_info:
        column_comments = [col['column_comment'] for col in table['columns']]
        table_comment = generate_comment_with_gptneo(gptneo_pipeline, column_comments)
        table['table_comment'] = table_comment

    with open(output_file, 'w') as f:
        json.dump(schema_info, f, indent=2, ensure_ascii=False)
    print(f"Comments generated for tables saved to {output_file}")

if __name__ == "__main__":
    input_file = './output/filtered_schema_info.json'
    output_file = './output/schema_with_table_comments_gpt_neo.json'
    gptneo_pipeline = configure_gptneo_pipeline()
    process_table_comments(input_file, output_file, gptneo_pipeline)