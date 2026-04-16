from flask import Blueprint, render_template, request, redirect, url_for, flash

bp = Blueprint('recipe', __name__, url_prefix='/recipes')

@bp.route('/explore')
def explore():
    """
    GET: 查詢預設/公開的食譜，並渲染探索頁面供使用者瀏覽與收藏。
    """
    pass

@bp.route('/<int:id>')
def detail(id):
    """
    GET: 取得單一食譜的詳細資料、食材清單、標籤與烹飪步驟。
    """
    pass

@bp.route('/new', methods=['GET', 'POST'])
def new():
    """
    GET: 顯示新增食譜表單。
    POST: 接收資料建立 Recipe、RecipeIngredient 以及綁定對應的 Tag，儲存後重導向至詳細頁面。
    """
    pass

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """
    GET: 顯示編輯表單並自動帶入原食譜與食材等關聯資料。
    POST: 更新 Recipe 資料庫，包含可能的食材、標籤變動。重導向至詳細頁。
    """
    pass

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    POST: 驗證授權後，從 DB 中刪除該筆食譜 (關聯清單會由於 cascade 自動刪除)。重導向至首頁。
    """
    pass

@bp.route('/<int:id>/cooking-mode')
def cooking_mode(id):
    """
    GET: 渲染專屬於該食譜的大字體互動式介面 (cooking_mode.html)。
    """
    pass
