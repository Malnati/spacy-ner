import json
import re

def generate_contextual_comment(column_name, data_type, is_primary_key, column_default):
    # Sugere um comentário genérico baseado no nome da coluna, tipo de dados, chave primária e valor padrão
    comment = ""

    # Sugestões com base no nome da coluna
    if 'id' in column_name.lower():
        comment = "Identificador único para o registro." if is_primary_key else "Identificador relacionado ao registro."
    elif 'date' in column_name.lower() or 'time' in column_name.lower():
        comment = "Data e hora associada ao registro."
    elif 'code' in column_name.lower():
        comment = "Código associado ao registro."
    elif 'amount' in column_name.lower() or 'value' in column_name.lower():
        comment = "Valor numérico associado ao registro."
    elif 'name' in column_name.lower():
        comment = "Nome ou título associado ao registro."
    elif 'status' in column_name.lower():
        comment = "Indica o status atual do registro."
    elif 'description' in column_name.lower():
        comment = "Descrição detalhada do registro."
    elif 'type' in column_name.lower():
        comment = "Tipo ou categoria do registro."
    elif 'city' in column_name.lower():
        comment = "Nome da cidade associada ao registro."
    elif 'country' in column_name.lower():
        comment = "País associado ao registro."
    else:
        comment = f"Coluna {column_name} armazenando valores do tipo {data_type}."

    # Acrescentar informações adicionais com base em outros metadados
    if is_primary_key:
        comment += " Este campo é a chave primária."
    if column_default:
        comment += f" Valor padrão: {column_default}."

    return comment

def clean_comment(comment):
    # Limpar o comentário de qualquer redundância ou informação extra
    comment = re.sub(r'\s+', ' ', comment).strip()
    return comment

def filter_comments(input_file, output_file):
    # Ler o arquivo JSON com as informações do esquema
    with open(input_file, 'r') as f:
        schema_info = json.load(f)

    # Gerar e limpar os comentários
    for table in schema_info:
        for column in table['columns']:
            # Gerar um comentário baseado nos metadados
            column['column_comment'] = generate_contextual_comment(
                column_name=column['column_name'],
                data_type=column['data_type'],
                is_primary_key=column['is_primary_key'],
                column_default=column['column_default']
            )

            # Limpar o comentário gerado
            column['column_comment'] = clean_comment(column['column_comment'])

    # Salvar o resultado filtrado
    with open(output_file, 'w') as f:
        json.dump(schema_info, f, indent=2, ensure_ascii=False)
    print(f"Filtered schema information saved to {output_file}")

# Caminhos dos arquivos de entrada e saída
input_file = './output/schema_info.json'
output_file = './output/filtered_schema_info.json'

filter_comments(input_file, output_file)