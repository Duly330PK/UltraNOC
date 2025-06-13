import os
import psycopg2

def initialize_database():
    db_url = os.getenv("DATABASE_URL", "postgresql://root:root@localhost/ultranoc")
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM pg_tables WHERE tablename = 'users'")
    result = cursor.fetchone()
    if not result:
        print("⚙️  Initialisiere DB aus init.sql...")
        with open("backend/init.sql", "r") as f:
            cursor.execute(f.read())
        conn.commit()
    else:
        print("✅ Datenbanktabellen bereits vorhanden.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    initialize_database()
