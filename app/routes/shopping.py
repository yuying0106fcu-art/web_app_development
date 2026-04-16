from flask import Blueprint, render_template, request, redirect, url_for, flash

bp = Blueprint('shopping', __name__, url_prefix='/shopping-list')

@bp.route('/')
def index():
    """
    GET: 列出當前使用者所有的購物清單。
    """
    pass

@bp.route('/<int:id>')
def detail(id):
    """
    GET: 顯示單筆清單內的待採買物品細項與勾選狀態。
    """
    pass

@bp.route('/generate/<int:recipe_id>', methods=['POST'])
def generate(recipe_id):
    """
    POST: 從指定食譜拉取對應食材資訊，將其轉換為 ShoppingItem 並加入現有或新的 ShoppingList 中。
    完成後重導向至該清單詳細頁面。
    """
    pass

@bp.route('/<int:list_id>/item/<int:item_id>', methods=['POST'])
def update_item(list_id, item_id):
    """
    POST: 更新清單內特定物品的狀態 (例如切換 is_bought 或更新 estimated_cost)。
    可接收前端 form 或是 JS API 發出的變更請求。
    """
    pass
