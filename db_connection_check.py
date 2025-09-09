import psycopg2
import os

username = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
localhost = os.getenv("POSTGRES_HOST")
try:
    conn = psycopg2.connect(
        dbname = "document_library",
        user=username,
        password=password,
        host=localhost,
        port = 5432 )

    print("Sucess!!")
    conn.close()
except Exception as e:
    print("Error!!")