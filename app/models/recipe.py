from .db import get_db_connection
from datetime import datetime

class Recipe:
    @staticmethod
    def create(title, ingredients, steps, source_url=None, personal_note=None):
        now = datetime.now().isoformat()
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO recipes (title, source_url, ingredients, steps, personal_note, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (title, source_url, ingredients, steps, personal_note, now, now))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            recipes = conn.execute('SELECT * FROM recipes ORDER BY created_at DESC').fetchall()
            return [dict(r) for r in recipes]

    @staticmethod
    def get_by_id(recipe_id):
        with get_db_connection() as conn:
            recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
            return dict(recipe) if recipe else None

    @staticmethod
    def update(recipe_id, title, ingredients, steps, source_url=None, personal_note=None):
        now = datetime.now().isoformat()
        with get_db_connection() as conn:
            conn.execute('''
                UPDATE recipes
                SET title = ?, source_url = ?, ingredients = ?, steps = ?, personal_note = ?, updated_at = ?
                WHERE id = ?
            ''', (title, source_url, ingredients, steps, personal_note, now, recipe_id))
            conn.commit()

    @staticmethod
    def delete(recipe_id):
        with get_db_connection() as conn:
            conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
            conn.commit()
            
    @staticmethod
    def search(keyword):
        with get_db_connection() as conn:
            like_keyword = f'%{keyword}%'
            recipes = conn.execute('''
                SELECT * FROM recipes 
                WHERE title LIKE ? OR ingredients LIKE ? OR steps LIKE ?
                ORDER BY created_at DESC
            ''', (like_keyword, like_keyword, like_keyword)).fetchall()
            return [dict(r) for r in recipes]
