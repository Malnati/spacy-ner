import psycopg2
import json
import os
from datetime import date, datetime

class SampleDataAdder:
    def __init__(self, config, schema_file, output_file):
        self.config = config
        self.schema_file = schema_file
        self.output_file = output_file

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

    def add_sample_data(self):
        # Carrega o arquivo schema_info.json
        if not os.path.exists(self.schema_file):
            print(f"Schema file {self.schema_file} not found.")
            return

        with open(self.schema_file, 'r') as file:
            schema_info = json.load(file)

        connection = self.connect_to_db()
        if not connection:
            return

        try:
            cursor = connection.cursor()
            # Adiciona amostras de dados para cada coluna
            for table in schema_info:
                table_name = table['table_name']
                for column in table['columns']:
                    column_name = column['column_name']
                    # Consulta para obter uma amostra de dados
                    sample_query = f"SELECT DISTINCT {column_name} FROM {table_name} LIMIT 5"
                    try:
                        cursor.execute(sample_query)
                        samples = [row[0] for row in cursor.fetchall()]
                        # Converter os tipos de dados para string, quando necessário
                        samples = [self.convert_to_serializable(sample) for sample in samples]
                        column['sample_data'] = samples
                    except Exception as error:
                        print(f"Error fetching sample data for {table_name}.{column_name}: {error}")
                        column['sample_data'] = []

            # Salva o schema_info.json atualizado
            self.save_updated_schema_info(schema_info)

        except Exception as error:
            print(f"Error while adding sample data: {error}")
        finally:
            connection.close()
            print("Database connection closed.")

    def convert_to_serializable(self, value):
        # Converte valores não serializáveis para uma forma que o JSON suporte
        if isinstance(value, (date, datetime)):
            return value.isoformat()
        return value

    def save_updated_schema_info(self, schema_info):
        with open(self.output_file, 'w') as file:
            json.dump(schema_info, file, indent=2)
        print(f"Updated schema information with sample data has been saved to {self.output_file}")

# Configuração do banco de dados
config = {
    'host': 'localhost',
    'port': 5432,
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres'
}

schema_file = './output/schema_info.json'
output_file = './output/schema_info_with_samples.json'

sample_data_adder = SampleDataAdder(config, schema_file, output_file)
sample_data_adder.add_sample_data()