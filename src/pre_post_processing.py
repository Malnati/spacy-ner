# pre_post_processing.py

def preprocess_comments(comments):
    # Realiza pré-processamento nos comentários, removendo redundâncias
    return [comment.strip().capitalize() for comment in comments]

def postprocess_generated_text(generated_text):
    # Remove texto repetido e formata corretamente
    processed_text = generated_text.replace("Reconhecido como", "").strip()
    return processed_text

if __name__ == "__main__":
    # Exemplo de uso
    example_comments = [
        " coluna id sem descrição definida. ",
        " por favor, forneça mais detalhes. "
    ]
    preprocessed = preprocess_comments(example_comments)
    print(f"Preprocessed comments: {preprocessed}")

    generated_text = "Reconhecido como ORG: Coluna id; Coluna id sem descrição definida."
    postprocessed = postprocess_generated_text(generated_text)
    print(f"Postprocessed text: {postprocessed}")