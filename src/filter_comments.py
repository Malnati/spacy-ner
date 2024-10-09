# filter_comments.py

import json

def filter_comments(schema_info):
    filtered_schema_info = []

    for table in schema_info:
        filtered_columns = []
        for column in table['columns']:
            comment = column['column_comment'] or "Sem descrição"

            # Filtrar comentários repetidos ou irrelevantes
            if "Sem descrição" in comment or "Por favor, forneça mais detalhes" in comment:
                continue

            # Adicionar a coluna filtrada
            filtered_columns.append(column)

        # Adicionar a tabela somente se tiver colunas relevantes
        if filtered_columns:
            table['columns'] = filtered_columns
            filtered_schema_info.append(table)

    return filtered_schema_info

def load_schema_info(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_filtered_schema_info(schema_info, file_path):
    with open(file_path, 'w') as file:
        json.dump(schema_info, file, indent=2)

if __name__ == "__main__":
    input_file = './output/schema_info.json'
    output_file = './output/filtered_schema_info.json'

    schema_info = load_schema_info(input_file)
    filtered_schema_info = filter_comments(schema_info)
    save_filtered_schema_info(filtered_schema_info, output_file)
    print(f"Filtered schema information saved to {output_file}")