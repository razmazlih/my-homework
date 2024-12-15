import base64
import psycopg2
from os import getenv

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
        decoded_value = base64.b64decode(value).decode('utf-8')  # פענוח לקידוד UTF-8
        return decoded_value
    except Exception as e:
        return f"Error decoding: {e}"

# פונקציה להדפסת הנתונים מתוך file_data
def print_file_data(doc_id):
    cursor = conn.cursor()
    cursor.execute("SELECT file_data FROM documents WHERE id = %s", (doc_id,))
    row = cursor.fetchone()
    
    if row:
        file_data = row[0]
        
        # אם התוכן מקודד ב-Base64, נבצע פענוח
        if file_data.startswith(b'base64,'):
            decoded_data = decode_base64(file_data[7:])  # הסרה של 'base64,' מההתחלה
            print(f"Decoded file data: {decoded_data}")
        else:
            print(f"File data: {file_data}")
    else:
        print(f"No file data found for document id {doc_id}")

    cursor.close()

# קריאה לפונקציה להדפיס את התוכן של file_data
doc_id = 1  # לדוגמה, מזהה המסמך שברצונך להדפיס את ה-file_data שלו
print_file_data(doc_id)

conn.close()