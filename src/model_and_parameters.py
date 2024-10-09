# model_and_parameters.py

from transformers import pipeline

def configure_bart_pipeline():
    # Configura o pipeline para o modelo BART com os parâmetros ajustados
    bart_pipeline = pipeline(
        "text2text-generation", 
        model="facebook/bart-large",
        max_length=300,
        num_return_sequences=1,
        truncation=True
    )
    return bart_pipeline

def generate_comment_with_bart(bart_pipeline, column_comments):
    input_text = " ".join(column_comments)
    result = bart_pipeline(
        f"Gerar um comentário detalhado para a tabela com base nas descrições fornecidas: {input_text}"
    )
    return result[0]['generated_text']

if __name__ == "__main__":
    # Exemplo de uso
    bart_pipeline = configure_bart_pipeline()
    example_comments = [
        "Coluna id sem descrição definida.",
        "Coluna country representa o país."
    ]
    table_comment = generate_comment_with_bart(bart_pipeline, example_comments)
    print(f"Generated table comment: {table_comment}")