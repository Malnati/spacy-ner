import psycopg2
import json
import os

class DbReader:
    def __init__(self, config, schema_path):
        self.config = config
        self.schema_path = schema_path

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

    def get_schema_info(self):
        connection = self.connect_to_db()
        if not connection:
            return

        try:
            cursor = connection.cursor()
            # Consultar tabelas
            tables_query = """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
            """
            cursor.execute(tables_query)
            tables = [row[0] for row in cursor.fetchall()]

            schema_info = []

            for table_name in tables:
                # Consultar colunas
                columns_query = f"""
                    SELECT
                        c.column_name,
                        c.data_type,
                        c.character_maximum_length,
                        c.is_nullable,
                        c.column_default,
                        pgd.description AS column_comment,
                        EXISTS (
                            SELECT 1
                            FROM information_schema.table_constraints tc
                            JOIN information_schema.key_column_usage kcu
                            ON tc.constraint_name = kcu.constraint_name
                            AND tc.table_schema = kcu.table_schema
                            WHERE tc.constraint_type = 'PRIMARY KEY'
                            AND tc.table_name = c.table_name
                            AND kcu.column_name = c.column_name
                        ) AS is_primary_key
                    FROM
                        information_schema.columns c
                    LEFT JOIN
                        pg_catalog.pg_statio_all_tables st ON c.table_schema = st.schemaname AND c.table_name = st.relname
                    LEFT JOIN
                        pg_catalog.pg_description pgd ON pgd.objoid = st.relid AND pgd.objsubid = c.ordinal_position
                    WHERE
                        c.table_schema = 'public' AND c.table_name = %s
                """
                cursor.execute(columns_query, (table_name,))
                columns = cursor.fetchall()

                schema_info.append({
                    'table_name': table_name,
                    'columns': [
                        {
                            'column_name': col[0],
                            'data_type': col[1],
                            'character_maximum_length': col[2],
                            'is_nullable': col[3],
                            'column_default': col[4],
                            'column_comment': col[5],
                            'is_primary_key': col[6]
                        }
                        for col in columns
                    ]
                })

            self.save_schema_info_to_file(schema_info)

        except Exception as error:
            print(f"Error while fetching schema info: {error}")
        finally:
            connection.close()
            print("Database connection closed.")

    def save_schema_info_to_file(self, schema_info):
        if not os.path.exists(self.schema_path):
            os.makedirs(self.schema_path)

        file_path = os.path.join(self.schema_path, "schema_info.json")
        with open(file_path, 'w') as f:
            json.dump(schema_info, f, indent=2)
        print(f"Schema information has been saved to {file_path}")

# Configuração do banco de dados
config = {
    'host': 'localhost',
    'port': 5432,
    'database': 'nome_do_banco',
    'user': 'usuario',
    'password': 'senha'
}

schema_path = './output'

db_reader = DbReader(config, schema_path)
db_reader.get_schema_info()