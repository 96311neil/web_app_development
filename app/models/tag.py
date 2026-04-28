from .db import get_db_connection
import sqlite3

class Tag:
    """處理標籤與食譜關聯的資料庫操作"""

    @staticmethod
    def create(name):
        """
        新增一個標籤
        :param name: 標籤名稱
        :return: 標籤的 ID (若已存在則回傳現有 ID)，失敗回傳 None
        """
        try:
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
        except sqlite3.Error as e:
            print(f"Error creating tag: {e}")
            return None

    @staticmethod
    def get_all():
        """
        取得所有標籤，依名稱排序
        :return: 標籤字典列表
        """
        try:
            with get_db_connection() as conn:
                tags = conn.execute('SELECT * FROM tags ORDER BY name').fetchall()
                return [dict(t) for t in tags]
        except sqlite3.Error as e:
            print(f"Error getting all tags: {e}")
            return []

    @staticmethod
    def get_by_id(tag_id):
        """
        根據 ID 取得標籤
        :param tag_id: 標籤 ID
        :return: 標籤字典，若找不到則回傳 None
        """
        try:
            with get_db_connection() as conn:
                tag = conn.execute('SELECT * FROM tags WHERE id = ?', (tag_id,)).fetchone()
                return dict(tag) if tag else None
        except sqlite3.Error as e:
            print(f"Error getting tag {tag_id}: {e}")
            return None
            
    @staticmethod
    def get_by_recipe_id(recipe_id):
        """
        取得指定食譜所擁有的所有標籤
        :param recipe_id: 食譜 ID
        :return: 標籤字典列表
        """
        try:
            with get_db_connection() as conn:
                tags = conn.execute('''
                    SELECT tags.* FROM tags
                    JOIN recipe_tags ON tags.id = recipe_tags.tag_id
                    WHERE recipe_tags.recipe_id = ?
                ''', (recipe_id,)).fetchall()
                return [dict(t) for t in tags]
        except sqlite3.Error as e:
            print(f"Error getting tags for recipe {recipe_id}: {e}")
            return []

    @staticmethod
    def add_to_recipe(recipe_id, tag_id):
        """
        將標籤綁定到指定的食譜
        :param recipe_id: 食譜 ID
        :param tag_id: 標籤 ID
        :return: 布林值，表示是否綁定成功
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                # 避免重複關聯
                existing = cursor.execute('SELECT id FROM recipe_tags WHERE recipe_id = ? AND tag_id = ?', 
                                          (recipe_id, tag_id)).fetchone()
                if not existing:
                    cursor.execute('INSERT INTO recipe_tags (recipe_id, tag_id) VALUES (?, ?)', (recipe_id, tag_id))
                    conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error adding tag {tag_id} to recipe {recipe_id}: {e}")
            return False

    @staticmethod
    def remove_from_recipe(recipe_id, tag_id):
        """
        將標籤從指定的食譜移除
        :param recipe_id: 食譜 ID
        :param tag_id: 標籤 ID
        :return: 布林值，表示是否移除成功
        """
        try:
            with get_db_connection() as conn:
                conn.execute('DELETE FROM recipe_tags WHERE recipe_id = ? AND tag_id = ?', (recipe_id, tag_id))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error removing tag {tag_id} from recipe {recipe_id}: {e}")
            return False
