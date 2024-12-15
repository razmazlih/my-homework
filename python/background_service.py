import time
import pandas as pd
import psycopg2
from os import getenv


conn = psycopg2.connect(
    dbname=getenv("DB_NAME", "my_database"),
    user=getenv("DB_USER","my_username"),
    password=getenv("DB_PASSWORD","my_password"),
    host=getenv("DB_HOST","localhost"),
    port=getenv("DB_PORT","5432")
)

def process_documents():
    while True:
        cursor = conn.cursor()
        cursor.execute("SELECT id, filename FROM documents WHERE status = 'uploaded' LIMIT 1")
        doc = cursor.fetchone()

        if doc:
            doc_id, filename = doc
            cursor.execute("UPDATE documents SET status = 'processing' WHERE id = %s", (doc_id,))
            conn.commit()

            try:
                processed_filename = filename.upper()
                processed_length = len(filename)

                cursor.execute(
                    "INSERT INTO processed_data (document_id, column1, column2) VALUES (%s, %s, %s)",
                    (doc_id, processed_filename, processed_length)
                )
                cursor.execute("UPDATE documents SET status = 'completed' WHERE id = %s", (doc_id,))
            except Exception as e:
                cursor.execute("UPDATE documents SET status = 'failed' WHERE id = %s", (doc_id,))
                print(f"Error processing document {doc_id}: {e}")
            conn.commit()
        else:
            time.sleep(5)

process_documents()