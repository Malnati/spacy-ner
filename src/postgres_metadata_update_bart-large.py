import json
import psycopg2
import spacy
from transformers import pipeline

class DatabaseUpdater:
    def __init__(self, config, schema_file):
        self.config = config
        self.schema_file = schema_file
        self.nlp = spacy.load("en_core_web_trf")
        # Configurar o pipeline para BART
        self.bart_pipeline = pipeline("text2text-generation", model="facebook/bart-large")

    def connect_to_db(self):
        try:
            connection = psycopg2.connect(
                host=self.config['host'],
                port=self.config['port'],
                database=self.config['database'],
                user=self.config['user'],
                password=self.config['password']
            )
            print("Connected to the database successfully.")
            return connection
        except Exception as error:
            print(f"Error connecting to the database: {error}")
            return None

    def load_schema_info(self):
        with open(self.schema_file, 'r') as file:
            schema_info = json.load(file)
        return schema_info

    def analyze_comments(self, comment):
        # Usar spaCy para melhorar o comentário
        doc = self.nlp(comment)
        insights = []
        for ent in doc.ents:
            insights.append(f"Reconhecido como {ent.label_}: {ent.text}")
        improved_comment = f"{comment} {'; '.join(insights)}"
        return improved_comment

    def generate_default_comment(self, column_name):
        # Gera uma descrição padrão se o comentário estiver ausente
        return f"Coluna {column_name} sem descrição definida. Por favor, forneça mais detalhes."

    def generate_table_comment_with_bart(self, column_comments):
        # Estruturar a entrada para o modelo com mais contexto
        input_text = "Descrição da tabela tb_chart. As colunas incluem: " + "; ".join(column_comments)
        result = self.bart_pipeline(
            f"Gerar um comentário detalhado para a tabela com base nas descrições fornecidas: {input_text}", 
            max_length=300,  
            max_new_tokens=150,  
            num_return_sequences=1,
            truncation=True
        )
        return result[0]['generated_text']

    def update_comments_in_db(self, connection, schema_info):
        try:
            cursor = connection.cursor()
            for table in schema_info:
                table_name = table['table_name']
                print(f"Atualizando comentários para a tabela: {table_name}")

                # Coletar os comentários das colunas para gerar o comentário da tabela
                column_comments = []
                
                # Atualizar comentários das colunas
                for column in table['columns']:
                    column_name = column['column_name']
                    original_comment = column['column_comment'] or self.generate_default_comment(column_name)
                    new_comment = self.analyze_comments(original_comment)

                    # Adicionar o novo comentário à lista de comentários das colunas
                    column_comments.append(new_comment)

                    update_query = f"""
                        COMMENT ON COLUMN {table_name}.{column_name} IS %s
                    """
                    cursor.execute(update_query, (new_comment,))
                    print(f"Comentário atualizado para {table_name}.{column_name}: {new_comment}")

                # Gerar comentário para a tabela usando BART
                table_comment = self.generate_table_comment_with_bart(column_comments)
                cursor.execute(f"COMMENT ON TABLE {table_name} IS %s", (table_comment,))
                print(f"Comentário atualizado para a tabela {table_name}: {table_comment}")

            connection.commit()
            print("Comentários atualizados no banco de dados.")
        except Exception as error:
            print(f"Error while updating comments in the database: {error}")
        finally:
            cursor.close()

    def run(self):
        connection = self.connect_to_db()
        if not connection:
            return
        
        schema_info = self.load_schema_info()
        self.update_comments_in_db(connection, schema_info)
        
        connection.close()
        print("Database connection closed.")

# Configuração do banco de dados
config = {
    'host': 'localhost',
    'port': 5432,
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres'
}

schema_file = './output/schema_info.json'

db_updater = DatabaseUpdater(config, schema_file)
db_updater.run()