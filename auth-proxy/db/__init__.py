import os
from .postgres import PostgresDB
# from .mysql import MySQLDB   # future
# from .mongo import MongoDB   # future

def get_database():
    """Factory to choose DB backend dynamically via .env"""
    db_type = os.getenv("DB_TYPE", "postgres").lower()

    if db_type == "postgres":
        return PostgresDB()
    # elif db_type == "mysql":
    #     return MySQLDB()
    # elif db_type == "mongodb":
    #     return MongoDB()
    else:
        raise ValueError(f"Unsupported DB_TYPE: {db_type}")
