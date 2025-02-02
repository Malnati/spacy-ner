import json
import torch 
from transformers import GPTJForCausalLM, AutoTokenizer, pipeline

cache_dir = "/usr/src/app/models"

def check_system_requirements(model_name):
    # Recommended memory: 24-32 GB GPU VRAM, 32 GB system RAM
    min_vram_gptj = 24 * 1024  # in MB
    min_ram_gptj = 32 * 1024   # in MB

    # Check if GPU is available
    if torch.cuda.is_available():
        total_vram = torch.cuda.get_device_properties(0).total_memory / (1024 * 1024)  # Convert bytes to MB
        if total_vram < min_vram_gptj:
            raise RuntimeError(f"Insufficient GPU memory. Required: {min_vram_gptj} MB, Available: {total_vram:.2f} MB")
        print(f"GPU memory check passed. Available VRAM: {total_vram:.2f} MB")
    else:
        # Fallback to checking system RAM if GPU is not available
        import psutil
        total_ram = psutil.virtual_memory().total / (1024 * 1024)  # Convert bytes to MB
        if total_ram < min_ram_gptj:
            raise RuntimeError(f"Insufficient system memory. Required: {min_ram_gptj} MB, Available: {total_ram:.2f} MB")
        print(f"System memory check passed. Available RAM: {total_ram:.2f} MB")

def configure_gptj_pipeline():
    model_name = "EleutherAI/gpt-j-6B"
    check_system_requirements(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
    model = GPTJForCausalLM.from_pretrained(model_name, cache_dir=cache_dir)
    # Use GPU if available
    gptj_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1, cache_dir=cache_dir)
    return gptj_pipeline

def generate_comment_with_gptj(gptj_pipeline, column_comments):
    input_text = ". ".join(column_comments)
    # Generate comments with a limited number of new tokens to avoid issues
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