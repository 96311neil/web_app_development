from .db import get_db_connection
from datetime import datetime
import sqlite3

class Recipe:
    """處理食譜的相關資料庫操作"""
    
    @staticmethod
    def create(title, ingredients, steps, source_url=None, personal_note=None):
        """
        新增一筆食譜記錄
        :param title: 食譜名稱
        :param ingredients: 食材清單
        :param steps: 製作步驟
        :param source_url: 來源網址
        :param personal_note: 個人筆記
        :return: 新增的食譜 ID，若失敗則回傳 None
        """
        now = datetime.now().isoformat()
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO recipes (title, source_url, ingredients, steps, personal_note, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (title, source_url, ingredients, steps, personal_note, now, now))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error creating recipe: {e}")
            return None

    @staticmethod
    def get_all():
        """
        取得所有食譜記錄，依建立時間降序排列
        :return: 食譜字典列表
        """
        try:
            with get_db_connection() as conn:
                recipes = conn.execute('SELECT * FROM recipes ORDER BY created_at DESC').fetchall()
                return [dict(r) for r in recipes]
        except sqlite3.Error as e:
            print(f"Error getting all recipes: {e}")
            return []

    @staticmethod
    def get_by_id(recipe_id):
        """
        根據 ID 取得單筆食譜記錄
        :param recipe_id: 食譜 ID
        :return: 食譜字典，若找不到則回傳 None
        """
        try:
            with get_db_connection() as conn:
                recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
                return dict(recipe) if recipe else None
        except sqlite3.Error as e:
            print(f"Error getting recipe {recipe_id}: {e}")
            return None

    @staticmethod
    def update(recipe_id, title, ingredients, steps, source_url=None, personal_note=None):
        """
        更新指定的食譜記錄
        :param recipe_id: 食譜 ID
        :param title: 食譜名稱
        :param ingredients: 食材清單
        :param steps: 製作步驟
        :param source_url: 來源網址
        :param personal_note: 個人筆記
        :return: 布林值，表示是否更新成功
        """
        now = datetime.now().isoformat()
        try:
            with get_db_connection() as conn:
                conn.execute('''
                    UPDATE recipes
                    SET title = ?, source_url = ?, ingredients = ?, steps = ?, personal_note = ?, updated_at = ?
                    WHERE id = ?
                ''', (title, source_url, ingredients, steps, personal_note, now, recipe_id))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error updating recipe {recipe_id}: {e}")
            return False

    @staticmethod
    def delete(recipe_id):
        """
        刪除指定的食譜記錄
        :param recipe_id: 食譜 ID
        :return: 布林值，表示是否刪除成功
        """
        try:
            with get_db_connection() as conn:
                conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error deleting recipe {recipe_id}: {e}")
            return False
            
    @staticmethod
    def search(keyword):
        """
        根據關鍵字搜尋食譜記錄 (名稱、食材、步驟)
        :param keyword: 搜尋字串
        :return: 搜尋到的食譜字典列表
        """
        try:
            with get_db_connection() as conn:
                like_keyword = f'%{keyword}%'
                recipes = conn.execute('''
                    SELECT * FROM recipes 
                    WHERE title LIKE ? OR ingredients LIKE ? OR steps LIKE ?
                    ORDER BY created_at DESC
                ''', (like_keyword, like_keyword, like_keyword)).fetchall()
                return [dict(r) for r in recipes]
        except sqlite3.Error as e:
            print(f"Error searching recipes with keyword '{keyword}': {e}")
            return []
