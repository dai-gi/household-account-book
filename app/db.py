import sqlite3

import click
from flask import current_app, g

def get_db():
  if 'db' not in g:
    # データベース接続を作成
    g.db = sqlite3.connect(
      # 指定されたデータベースファイルに接続
      current_app.config['DATABASE'],
      # SQLiteのデータ型をPythonのデータ型に変換する
      detect_types=sqlite3.PARSE_DECLTYPES
    )
    # クエリの結果を辞書のように扱うことができる
    g.db.row_factory = sqlite3.Row

  return g.db


def close_db(e=None):
  # `g`オブジェクトからデータベース接続を取り出す
  # 接続が存在しない場合、`None`を返す
  db = g.pop('db', None)

  # `db`が存在する場合にデータベースを閉じる
  if db is not None:
    db.close()


def init_db():
  db = get_db()
  
  # appフォルダからschema.sqlファイルを開く
  with current_app.open_resource('schema.sql') as f:
  
    # schema.sqlファイルの内容をデータベースに実行することでデータベースのスキーマ（テーブル定義など）が設定される
    db.executescript(f.read().decode('utf8'))


# init-dbという名前のCLIコマンドとして登録される
@click.command('init-db')
def init_db_command():
  init_db()
  # 'Initialized the database.'というメッセージを出力される。
  click.echo('Initialized the database.')


def init_app(app):
  # リクエストが終わった後に呼ばれる関数を登録する
  app.teardown_appcontext(close_db)

  #  `init_db_command`関数を新しいコマンドとして追加する
  app.cli.add_command(init_db_command)