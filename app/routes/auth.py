import functools
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    """在每次 Request 執行前，確認 session 中有沒有 user_id 並放進 g.user 中"""
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.get_by_id(user_id)

def login_required(view):
    """
    自訂裝飾器：限制必須登入後才能存取頁面
    如果沒登入就會重導向回登入頁。
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("請先登入才能繼續操作。", "warning")
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    GET: 顯示註冊表單。
    POST: 接收表單資料，驗證與防止帳號重複，建立新使用者至資料庫，重導向至登入頁。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        error = None

        if not username:
            error = '帳號為必填。'
        elif not email:
            error = '信箱為必填。'
        elif not password:
            error = '密碼為必填。'
        
        if error is None:
            existing_user = User.get_by_username(username)
            if existing_user is None:
                pw_hash = generate_password_hash(password)
                user = User.create(username=username, email=email, password_hash=pw_hash)
                if user:
                    flash('註冊成功！請登入。', 'success')
                    return redirect(url_for('auth.login'))
                else:
                    error = '系統發生錯誤，無法註冊。'
            else:
                error = f"帳號 {username} 已經有人使用了。"
        
        flash(error, 'danger')

    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET: 顯示登入表單。
    POST: 驗證使用者帳號密碼，成功則將使用者 ID 寫入 session，重導至首頁。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None
        
        user = User.get_by_username(username)

        if user is None:
            error = '找不到此帳號。'
        elif not check_password_hash(user.password_hash, password):
            error = '密碼錯誤。'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            flash('登入成功！', 'success')
            return redirect(url_for('main.index'))
        
        flash(error, 'danger')

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    """
    將使用者 ID 從 session 中移除，登出並重導回登入頁。
    """
    session.clear()
    flash('您已成功登出。', 'info')
    return redirect(url_for('auth.login'))
