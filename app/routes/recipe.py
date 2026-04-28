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
    q = request.args.get('q', '').strip()
    tag_name = request.args.get('tag', '').strip()
    
    # 根據關鍵字搜尋或取得全部
    if q:
        recipes = Recipe.search(q)
    else:
        recipes = Recipe.get_all()
        
    # 如果有標籤過濾
    if tag_name:
        all_tags = Tag.get_all()
        target_tag = next((t for t in all_tags if t['name'] == tag_name), None)
        if target_tag:
            filtered_recipes = []
            for r in recipes:
                r_tags = Tag.get_by_recipe_id(r['id'])
                if any(rt['id'] == target_tag['id'] for rt in r_tags):
                    filtered_recipes.append(r)
            recipes = filtered_recipes
        else:
            recipes = [] # 找不到該標籤
            
    # 取出所有標籤供側邊欄或篩選顯示
    all_tags = Tag.get_all()
    
    return render_template('index.html', recipes=recipes, tags=all_tags, q=q, current_tag=tag_name)

@recipe_bp.route('/recipes/new')
def new():
    """
    處理 GET /recipes/new
    邏輯：獲取所有標籤，準備渲染新增表單
    輸出：渲染 templates/form.html
    """
    all_tags = Tag.get_all()
    return render_template('form.html', action="create", tags=all_tags)

@recipe_bp.route('/recipes', methods=['POST'])
def create():
    """
    處理 POST /recipes
    輸入：表單資料
    邏輯：呼叫 Recipe.create() 新增資料，並處理標籤綁定
    輸出：重導向至 index
    """
    title = request.form.get('title', '').strip()
    source_url = request.form.get('source_url', '').strip()
    ingredients_text = request.form.get('ingredients', '').strip()
    steps = request.form.get('steps', '').strip()
    personal_note = request.form.get('personal_note', '').strip()
    
    # 輸入驗證
    if not title or not ingredients_text or not steps:
        flash('食譜名稱、食材清單與製作步驟為必填！', 'danger')
        all_tags = Tag.get_all()
        # 回到表單並保留填寫的資料
        return render_template('form.html', action="create", tags=all_tags, 
                               recipe={'title': title, 'source_url': source_url, 
                                       'ingredients': ingredients_text, 'steps': steps, 
                                       'personal_note': personal_note})
                                       
    recipe_id = Recipe.create(title, ingredients_text, steps, source_url, personal_note)
    
    if recipe_id:
        # 處理標籤輸入 (以逗號分隔)
        tags_input = request.form.get('tags', '').strip()
        if tags_input:
            tag_names = [t.strip() for t in tags_input.split(',') if t.strip()]
            for name in tag_names:
                tag_id = Tag.create(name)
                if tag_id:
                    Tag.add_to_recipe(recipe_id, tag_id)
        
        flash('成功新增食譜！', 'success')
        return redirect(url_for('recipe.index'))
    else:
        flash('新增失敗，請稍後再試。', 'danger')
        all_tags = Tag.get_all()
        return render_template('form.html', action="create", tags=all_tags)

@recipe_bp.route('/recipes/<int:id>')
def detail(id):
    """
    處理 GET /recipes/<id>
    輸入：食譜 ID
    邏輯：獲取單筆食譜資料與標籤
    輸出：渲染 templates/detail.html
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜！', 'danger')
        return redirect(url_for('recipe.index'))
        
    tags = Tag.get_by_recipe_id(id)
    return render_template('detail.html', recipe=recipe, tags=tags)

@recipe_bp.route('/recipes/<int:id>/edit')
def edit(id):
    """
    處理 GET /recipes/<id>/edit
    輸入：食譜 ID
    邏輯：獲取欲編輯的食譜資料，準備表單
    輸出：渲染 templates/form.html
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜！', 'danger')
        return redirect(url_for('recipe.index'))
        
    recipe_tags = Tag.get_by_recipe_id(id)
    all_tags = Tag.get_all()
    
    # 組合當前標籤供表單顯示
    tags_string = ", ".join([t['name'] for t in recipe_tags])
    recipe_dict = dict(recipe)
    recipe_dict['tags_string'] = tags_string
    
    return render_template('form.html', action="edit", recipe=recipe_dict, tags=all_tags)

@recipe_bp.route('/recipes/<int:id>/update', methods=['POST'])
def update(id):
    """
    處理 POST /recipes/<id>/update
    輸入：食譜 ID 與表單資料
    邏輯：呼叫 Recipe.update() 更新資料與標籤關聯
    輸出：重導向至 detail 頁面
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜！', 'danger')
        return redirect(url_for('recipe.index'))

    title = request.form.get('title', '').strip()
    source_url = request.form.get('source_url', '').strip()
    ingredients_text = request.form.get('ingredients', '').strip()
    steps = request.form.get('steps', '').strip()
    personal_note = request.form.get('personal_note', '').strip()
    
    if not title or not ingredients_text or not steps:
        flash('食譜名稱、食材清單與製作步驟為必填！', 'danger')
        return redirect(url_for('recipe.edit', id=id))
        
    success = Recipe.update(id, title, ingredients_text, steps, source_url, personal_note)
    
    if success:
        # 更新標籤：先刪除舊有關聯，再新增
        old_tags = Tag.get_by_recipe_id(id)
        for t in old_tags:
            Tag.remove_from_recipe(id, t['id'])
            
        tags_input = request.form.get('tags', '').strip()
        if tags_input:
            tag_names = [t.strip() for t in tags_input.split(',') if t.strip()]
            for name in tag_names:
                tag_id = Tag.create(name)
                if tag_id:
                    Tag.add_to_recipe(id, tag_id)
                    
        flash('成功更新食譜！', 'success')
        return redirect(url_for('recipe.detail', id=id))
    else:
        flash('更新失敗，請稍後再試。', 'danger')
        return redirect(url_for('recipe.edit', id=id))

@recipe_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    處理 POST /recipes/<id>/delete
    輸入：食譜 ID
    邏輯：呼叫 Recipe.delete()
    輸出：重導向至 index
    """
    success = Recipe.delete(id)
    if success:
        flash('食譜已刪除！', 'success')
    else:
        flash('刪除失敗或食譜不存在！', 'danger')
    return redirect(url_for('recipe.index'))

@recipe_bp.route('/recipes/<int:id>/ingredients')
def ingredients(id):
    """
    處理 GET /recipes/<id>/ingredients
    輸入：食譜 ID
    邏輯：獲取食譜食材部分
    輸出：渲染 templates/ingredients.html (採買清單模式)
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜！', 'danger')
        return redirect(url_for('recipe.index'))
        
    return render_template('ingredients.html', recipe=recipe)
