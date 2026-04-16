from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """
    若使用者已登入，顯示個人首頁(食譜收藏與近期清單)。
    若未登入，顯示系統介紹或將其重導向至登入頁面。
    """
    pass
