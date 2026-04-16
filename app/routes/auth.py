from flask import Blueprint, render_template, request, redirect, url_for, flash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    GET: 顯示註冊表單。
    POST: 接收表單資料，驗證與防止帳號重複，建立新使用者至資料庫，重導向至登入頁。
    """
    pass

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET: 顯示登入表單。
    POST: 驗證使用者帳號密碼，成功則將使用者 ID 寫入 session，重導至首頁。
    """
    pass

@bp.route('/logout')
def logout():
    """
    將使用者 ID 從 session 中移除，登出並重導回登入頁。
    """
    pass
