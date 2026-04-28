from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.recipe import Recipe
from app.models.tag import Tag

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/')
@recipe_bp.route('/recipes')
def index():
    """
    處理 GET / 與 GET /recipes
    輸入：URL 參數 q (搜尋) 或 tag (過濾)
    邏輯：呼叫 Recipe.get_all() 或 search() 獲取列表
    輸出：渲染 templates/index.html
    """
    pass

@recipe_bp.route('/recipes/new')
def new():
    """
    處理 GET /recipes/new
    邏輯：獲取所有標籤，準備渲染新增表單
    輸出：渲染 templates/form.html
    """
    pass

@recipe_bp.route('/recipes', methods=['POST'])
def create():
    """
    處理 POST /recipes
    輸入：表單資料
    邏輯：呼叫 Recipe.create() 新增資料，並處理標籤綁定
    輸出：重導向至 index
    """
    pass

@recipe_bp.route('/recipes/<int:id>')
def detail(id):
    """
    處理 GET /recipes/<id>
    輸入：食譜 ID
    邏輯：獲取單筆食譜資料與標籤
    輸出：渲染 templates/detail.html
    """
    pass

@recipe_bp.route('/recipes/<int:id>/edit')
def edit(id):
    """
    處理 GET /recipes/<id>/edit
    輸入：食譜 ID
    邏輯：獲取欲編輯的食譜資料，準備表單
    輸出：渲染 templates/form.html
    """
    pass

@recipe_bp.route('/recipes/<int:id>/update', methods=['POST'])
def update(id):
    """
    處理 POST /recipes/<id>/update
    輸入：食譜 ID 與表單資料
    邏輯：呼叫 Recipe.update() 更新資料與標籤關聯
    輸出：重導向至 detail 頁面
    """
    pass

@recipe_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    處理 POST /recipes/<id>/delete
    輸入：食譜 ID
    邏輯：呼叫 Recipe.delete()
    輸出：重導向至 index
    """
    pass

@recipe_bp.route('/recipes/<int:id>/ingredients')
def ingredients(id):
    """
    處理 GET /recipes/<id>/ingredients
    輸入：食譜 ID
    邏輯：獲取食譜食材部分
    輸出：渲染 templates/ingredients.html (採買清單模式)
    """
    pass
