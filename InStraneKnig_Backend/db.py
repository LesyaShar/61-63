import pyodbc
import os
from dotenv import load_dotenv


# Загружаем .env
load_dotenv()


def get_db_connection():
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    driver = os.getenv("DB_DRIVER")

    print("=== ДАННЫЕ ПОДКЛЮЧЕНИЯ ===")
    print("SERVER:", server)
    print("DATABASE:", database)
    print("DRIVER:", driver)
    print("===========================")

    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    print("Строка подключения сформирована.")

    try:
        connection = pyodbc.connect(connection_string)

        print("✅ Flask подключился к SQL Server")

        return connection

    except pyodbc.Error as e:
        print("❌ Ошибка подключения к БД:")
        print(e)

        return None