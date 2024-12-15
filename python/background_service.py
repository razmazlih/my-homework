import time
import pandas as pd
import psycopg2
from os import getenv
import base64


# חיבור למסד הנתונים
conn = psycopg2.connect(
    dbname=getenv("DB_NAME", "my_database"),
    user=getenv("DB_USER", "my_username"),
    password=getenv("DB_PASSWORD", "my_password"),
    host=getenv("DB_HOST", "localhost"),
    port=getenv("DB_PORT", "5432")
)


# פונקציה לניתוח תוכן הקלט (Base64 או טקסט רגיל)
def analyze_content(input_string):
    try:
        decoded_bytes = base64.b64decode(input_string, validate=True)
        decoded_text = decoded_bytes.decode('utf-8')
        return {
            "type": "base64",
            "content": decoded_text
        }
    except (base64.binascii.Error, UnicodeDecodeError):
        return {
            "type": "plain",
            "content": input_string
        }


# פונקציה לעיבוד המסמכים
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
                # ניתוח שם הקובץ
                analysis_result = analyze_content(filename)
                processed_filename = analysis_result['content']
                processed_type = analysis_result['type']

                # שמירת המידע המעובד בטבלת processed_data
                cursor.execute(
                    """
                    INSERT INTO processed_data (document_id, column1, column2)
                    VALUES (%s, %s, %s)
                    """,
                    (doc_id, processed_filename, processed_type)
                )

                # עדכון סטטוס ל-completed
                cursor.execute(
                    "UPDATE documents SET status = 'completed' WHERE id = %s",
                    (doc_id,)
                )

            except Exception as e:
                # עדכון סטטוס ל-failed במקרה של שגיאה
                cursor.execute(
                    "UPDATE documents SET status = 'failed' WHERE id = %s",
                    (doc_id,)
                )
                print(f"Error processing document {doc_id}: {e}")
            
            finally:
                conn.commit()
        else:
            # אם אין מסמכים חדשים, להמתין 5 שניות
            time.sleep(5)


# הפעלת עיבוד המסמכים
process_documents()