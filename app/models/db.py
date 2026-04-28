import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../../instance/database.db')

def get_db_connection():
    """
    建立並回傳 SQLite 資料庫連線。
    預設啟用 foreign keys 支援，並設定 row_factory 為 sqlite3.Row。
    """
    try:
        # 確保 instance 目錄存在
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        # 啟用外鍵支援
        conn.execute('PRAGMA foreign_keys = ON')
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        raise

def init_db():
    """
    初始化資料庫，讀取 schema.sql 並執行建表語法。
    """
    try:
        schema_path = os.path.join(os.path.dirname(__file__), '../../database/schema.sql')
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = f.read()
        with get_db_connection() as conn:
            conn.executescript(schema)
    except Exception as e:
        print(f"Database initialization error: {e}")
        raise
