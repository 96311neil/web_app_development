from .db import get_db_connection
import sqlite3

class Tag:
    @staticmethod
    def create(name):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO tags (name) VALUES (?)', (name,))
                conn.commit()
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                # 標籤已存在，回傳現有的 ID
                tag = conn.execute('SELECT id FROM tags WHERE name = ?', (name,)).fetchone()
                return tag['id']

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            tags = conn.execute('SELECT * FROM tags ORDER BY name').fetchall()
            return [dict(t) for t in tags]

    @staticmethod
    def get_by_id(tag_id):
        with get_db_connection() as conn:
            tag = conn.execute('SELECT * FROM tags WHERE id = ?', (tag_id,)).fetchone()
            return dict(tag) if tag else None
            
    @staticmethod
    def get_by_recipe_id(recipe_id):
        with get_db_connection() as conn:
            tags = conn.execute('''
                SELECT tags.* FROM tags
                JOIN recipe_tags ON tags.id = recipe_tags.tag_id
                WHERE recipe_tags.recipe_id = ?
            ''', (recipe_id,)).fetchall()
            return [dict(t) for t in tags]

    @staticmethod
    def add_to_recipe(recipe_id, tag_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # 避免重複關聯
            existing = cursor.execute('SELECT id FROM recipe_tags WHERE recipe_id = ? AND tag_id = ?', 
                                      (recipe_id, tag_id)).fetchone()
            if not existing:
                cursor.execute('INSERT INTO recipe_tags (recipe_id, tag_id) VALUES (?, ?)', (recipe_id, tag_id))
                conn.commit()

    @staticmethod
    def remove_from_recipe(recipe_id, tag_id):
        with get_db_connection() as conn:
            conn.execute('DELETE FROM recipe_tags WHERE recipe_id = ? AND tag_id = ?', (recipe_id, tag_id))
            conn.commit()
