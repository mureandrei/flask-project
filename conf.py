import os


DB_FILE_PATH = os.getenv("DB_FILE_PATH", f"{os.getcwd()}/data.db")
GRAPHQL_SCHEMA_PATH = os.getenv("GRAPHQL_SCHEMA_PATH", "models/schema.graphql")
