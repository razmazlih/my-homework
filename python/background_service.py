import base64
import psycopg2
from os import getenv
from time import sleep

# הגדרת החיבור ל-PostgreSQL
conn = psycopg2.connect(
    dbname=getenv("DB_NAME", "my_database"),
    user=getenv("DB_USER", "my_username"),
    password=getenv("DB_PASSWORD", "my_password"),
    host=getenv("DB_HOST", "localhost"),
    port=getenv("DB_PORT", "5432")
)

# פונקציה לפענוח נתונים מקודדים ב-base64
def decode_base64(value):
    try:
        decoded_value = base64.b64decode(value).decode('utf-8')
        return decoded_value
    except Exception as e:
        return f"Error decoding: {e}"

# פונקציה שמכניסה את הנתונים המפוענחים לטבלה processed_data
def insert_processed_data(doc_id, column1, column2):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO processed_data (document_id, column1, column2) VALUES (%s, %s, %s)",
        (doc_id, column1, column2)
    )
    conn.commit()
    cursor.close()

# פונקציה לעיבוד המסמך
def process_document(doc_id):
    print(f"Processing document {doc_id}")
    cursor = conn.cursor()

    # עדכון סטטוס למסמך ל-"processing"
    cursor.execute("UPDATE documents SET status = 'processing' WHERE id = %s", (doc_id,))
    conn.commit()

    cursor.execute("SELECT id, column1, column2 FROM processed_data WHERE document_id = %s", (doc_id,))
    rows = cursor.fetchall()
    
    for row in rows:
        record_id = row[0]
        column1 = row[1]
        column2 = row[2]
        
        # אם הנתונים מקודדים ב-Base64, נבצע פענוח
        if column1.startswith("base64,"):
            column1 = decode_base64(column1[7:])  # הסרת "base64," מההתחלה
        if column2.startswith("base64,"):
            column2 = decode_base64(column2[7:])  # הסרת "base64," מההתחלה
        
        # שמירת הנתונים המפוענחים לטבלה processed_data
        insert_processed_data(doc_id, column1, column2)
        print(f"ID: {record_id}, Column1: {column1}, Column2: {column2}")
    
    cursor.close()

    # עדכון הסטטוס למסמך ל-"completed"
    cursor = conn.cursor()
    cursor.execute("UPDATE documents SET status = 'completed' WHERE id = %s", (doc_id,))
    conn.commit()
    cursor.close()

while True:
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM documents WHERE status = 'uploaded'")
    rows = cursor.fetchall()

    for row in rows:
        doc_id = row[0]
        print(f"Found document {doc_id} to be processed.")
        
        # קריאה לפונקציה לעיבוד המסמך
        process_document(doc_id)

    cursor.close()
    
    sleep(10)

conn.close()