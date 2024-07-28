import sqlite3

import click
from flask import current_app, g

def get_db():
  if 'db' not in g:
    # `g`オブジェクト：リクエストごとに一時的なデータを保存する。
    # `sqlite3.connect`：データベース接続を作成し、`current_app.config['DATABASE']`で指定されたデータベースファイルに接続する。
    g.db = sqlite3.connect(
      current_app.config['DATABASE'],
      # SQLiteの型を適切に解析する。
      detect_types=sqlite3.PARSE_DECLTYPES
    )
    # クエリの結果を辞書のように扱うことができるようになる。
    g.db.row_factory = sqlite3.Row

  return g.db


def close_db(e=None):
  # `g`オブジェクトからデータベース接続を取り出す。接続が存在しない場合、`None`を返す。
  db = g.pop('db', None)

  # `db`が存在する場合、`db.close()`によりデータベースを閉じる。
  if db is not None:
    db.close()


def init_db():
  db = get_db()
  
  # `current_app.open_resource('schema.sql')`により、アプリケーションのリソースフォルダから schema.sql ファイルを開く。
  with current_app.open_resource('schema.sql') as f:
  
    # `db.executescript`を使用して、schema.sql ファイルの内容をデータベースに実行します。これにより、データベースのスキーマ（テーブル定義など）が設定される。
    db.executescript(f.read().decode('utf8'))


# @click.command('init-db') デコレーターにより、この関数が init-db という名前のCLIコマンドとして登録される。
@click.command('init-db')
def init_db_command():
  # init_db 関数を呼び出してデータベースを初期化し、click.echo('Initialized the database.') により、「Initialized the database.」というメッセージを出力される。
  init_db()
  click.echo('Initialized the database.')


def init_app(app):
  # `teardown_appcontext`は、リクエストが終わった後に呼ばれる関数を登録するためのもの。
  app.teardown_appcontext(close_db)

  #  `init_db_command`関数を新しいコマンドとして追加するためのもの。
  app.cli.add_command(init_db_command)