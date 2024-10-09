# apply_rules.py

def apply_comment_rules(column):
    # Melhora os comentários com base nas características dos dados
    comment = column['column_comment'] or "Sem descrição"

    if column['is_primary_key']:
        comment += " Esta coluna é uma chave primária e identifica unicamente os registros."

    if "data_type" in column and column['data_type'] == "character varying":
        comment += " O campo aceita texto variável."

    return comment

def apply_rules_to_schema(schema_info):
    for table in schema_info:
        for column in table['columns']:
            column['column_comment'] = apply_comment_rules(column)

    return schema_info

def load_schema_info(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_enhanced_schema_info(schema_info, file_path):
    with open(file_path, 'w') as file:
        json.dump(schema_info, file, indent=2)

if __name__ == "__main__":
    input_file = './output/filtered_schema_info.json'
    output_file = './output/enhanced_schema_info.json'

    schema_info = load_schema_info(input_file)
    enhanced_schema_info = apply_rules_to_schema(schema_info)
    save_enhanced_schema_info(enhanced_schema_info, output_file)
    print(f"Enhanced schema information saved to {output_file}")