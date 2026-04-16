from flask import Blueprint, redirect, url_for, g

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """
    若使用者已登入，顯示歡迎訊息(因為首頁模板還沒建置)。
    若未登入，將其重導向至登入頁面。
    """
    if getattr(g, 'user', None):
        return f"""
        <html>
        <body style='background-color: #2c5364; color: white; padding: 50px; font-family: sans-serif;'>
            <h1>歡迎回來，{g.user.username}！</h1>
            <p>食譜管家首頁還在趕工中，請期待！</p>
            <a href='{url_for('auth.logout')}' style='color: #0dcaf0;'>登出</a>
        </body>
        </html>
        """
    return redirect(url_for('auth.login'))
