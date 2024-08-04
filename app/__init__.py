import os
from flask import Flask

def create_app(test_config=None):
    # `instance_relative_config=True`: アプリケーションがインスタンスフォルダという特殊なフォルダから設定ファイルを読み込むことを可能にする
    app = Flask(__name__, instance_relative_config=True)

    # アプリの設定を追加する
    app.config.from_mapping(
        # アプリの秘密の鍵
        SECRET_KEY='dev',
        # アプリが使うデータベースファイルの場所を指定する
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )
    print(app.instance_path)

    if test_config is None:
        # 追加の設定ファイル`config`を読み込みむ
        app.config.from_pyfile('config', silent=True)
    else:
        # `test_config`を設定に使う
        app.config.from_mapping(test_config)

    # インスタンスフォルダが既に存在した場合のエラーハンドリング
    try:
        # インスタンスフォルダを作成
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # `/hello`というURLにアクセスされたときに`hello`関数が呼ばれる
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # データベースを初期化する
    from . import db
    db.init_app(app)

    # 認証機能のブループリントをアプリに登録する
    from . import auth
    app.register_blueprint(auth.bp)

    # ブログ機能をのブループリントをアプリに登録する
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app