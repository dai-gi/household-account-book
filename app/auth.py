# 関数型プログラミングのためのツールを提供する
import functools

# Blueprint: 機能ごとにモジュール化して、コードを別々に管理する
# flash: ユーザーに一時的なメッセージを表示する
# g: リクエストごとに一時的なデータを保存するための特別なオブジェクト
# redirect: ユーザーを別のページにリダイレクトする
# render_template: HTMLテンプレートをレンダリングして、ユーザーにページを表示する
# request: 現在のリクエストに関する情報を提供する
# session: ユーザーのセッションデータを管理する
# url_for: URLを生成する
from flask import (
  Blueprint, flash, g, redirect, render_template, request, session, url_for
)

# check_password_hash: ハッシュ化されたパスワードをチェックするための関数
# generate_password_hash: パスワードをハッシュ化するための関数
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

# 認証に関する機能をまとめる新しいBlueprintオブジェクトを作成
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        
        if error is None:
            try:
                # データベースに対してSQLクエリを実行してデータを変更するための関数
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    # `?`プレースホルダーに後から値が埋め込まれる
                    (username, generate_password_hash(password))
                )
                # 変更を保存するための関数
                db.commit()
            # データベースの整合性制約に違反したときに発生するエラー
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                # ユーザーをログインURLに転送する
                return redirect(url_for('auth.login'))

        flash(error)

    # `register.html`をレンダリングして結果をレスポンスとして返す
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone() # クエリの結果から一行を返す関数

        if user is None:
            error = 'Incorrect username.'
        # ハッシュ化されたパスワードが正しいか判定している
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # 以前のセッションデータを消去する
            session.clear()
            # 現在ログインしているユーザーのIDをセッションに保存する
            session['user_id'] = user['id']
            # `index/`のURLに転送する
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

# 各リクエストの処理が始まる前に関数を実行する
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().excute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# ログインしているかどうかをチェックする
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view