import os
from flask import Flask

def create_app(test_config=None):
  # `instance_relative_config=True`は、アプリケーションがインスタンスフォルダという特殊なフォルダから設定ファイルを読み込むことを可能にする。
  # アプリケーションの設定をアプリケーションコードとは別の場所に置くことができる。
  app = Flask(__name__, instance_relative_config=True)

  # アプリの設定を追加する。
  app.config.from_mapping(
    # アプリの秘密の鍵で、セキュリティに使う。
    SECRET_KEY='dev',
    # アプリが使うデータベースのファイルの場所を指定する。
    DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
  )
  print(app.instance_path)

  # `test_config`が`None`ならば、追加の設定ファイル`config`を読み込みむ。そうでなければ、渡された`test_config`を設定に使う。
  if test_config is None:
    app.config.from_pyfile('config', silent=True)
  else:
    app.config.from_mapping(test_config)

  # `os.makedirs`でインスタンスフォルダを作成する。フォルダが既に存在する場合は`OSError`が発生するので、その場合は何もしないようにする。
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  # `@app.route('/hello')`で`/hello`というURLにアクセスされたときに`hello`関数が呼ばれる。
  @app.route('/hello')
  def hello():
    return 'Hello, World!'

  # データベースの初期化関数をインポートし、アプリのデータベースを初期化する。
  from . import db
  db.init_app(app)
  
  return app