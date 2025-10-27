import psycopg2
from psycopg2 import sql

DB_CONFIG = {
    'host': 'localhost',
    'port': '5433',
    'database': 'pereval',
    'user': 'postgres',
    'password': 'admin1'
}

def get_db_connection():
    """Создаёт подключение к БД"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Подключение к БД успешно!")
        return conn
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return None


if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT version();")
        print(cur.fetchone())
        cur.close()
        conn.close()