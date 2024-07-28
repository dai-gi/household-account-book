# household-account-book

## プロジェクト概要

家計簿アプリは、ユーザーが日々の収入と支出を記録し、家計の状況を簡単に把握できるようにするためのアプリケーションです。

## システム構成

### フロントエンド

- フレームワーク：Vue.js
- 機能：ユーザーインターフェース、データ入力フォーム、表示

### バックエンド

- 言語：Python
- フレームワーク：Flask または FastAPI
- 機能：API エンドポイント、データ処理、認証

### データベース

- システム：PostgreSQL
- 機能：収入と支出のデータ保存、ユーザー情報の管理

### インフラ

- クラウドサービス：AWS
- サービス：EC2（アプリケーションサーバー）、RDS（データベース）、S3（静的ファイルの保存）、IAM（認証・権限管理）

## 機能概要

### ユーザー管理

- 新規登録
- ログイン
- ログアウト

### 収入・支出管理

- 収入の登録
- 支出の登録
- 収入・支出の一覧表示
- 収入・支出の編集・削除

### レポート機能

- 月ごとの収支サマリー表示
- カテゴリー別支出グラフ

## データベース設計

### テーブル定義

- `users` テーブル

  - `id` (UUID, Primary Key)
  - `username` (VARCHAR, Unique)
  - `password` (VARCHAR)
  - `email` (VARCHAR, Unique)

- `transactions` テーブル
  - `id` (UUID, Primary Key)
  - `user_id` (UUID, Foreign Key)
  - `type` (VARCHAR) - `income`または`expense`
  - `amount` (NUMERIC)
  - `category` (VARCHAR)
  - `date` (DATE)
  - `description` (TEXT)

## API 設計

### エンドポイント一覧

- `POST /api/register` - 新規ユーザー登録
- `POST /api/login` - ユーザーログイン
- `POST /api/logout` - ユーザーログアウト
- `GET /api/transactions` - 収入・支出の一覧取得
- `POST /api/transactions` - 新規収入・支出の登録
- `PUT /api/transactions/{id}` - 収入・支出の編集
- `DELETE /api/transactions/{id}` - 収入・支出の削除
- `GET /api/reports/monthly` - 月ごとの収支サマリー取得

## フロントエンド設計

### ページ一覧

- ホームページ：ログイン・新規登録フォーム
- ダッシュボード：収入・支出の一覧表示、月ごとの収支サマリー表示
- 収入・支出登録ページ：収入・支出の新規登録フォーム
- レポートページ：カテゴリー別支出グラフ表示

### コンポーネント

- `Header.vue` - ヘッダーコンポーネント
- `Footer.vue` - フッターコンポーネント
- `LoginForm.vue` - ログインフォームコンポーネント
- `RegisterForm.vue` - 新規登録フォームコンポーネント
- `TransactionList.vue` - 収入・支出一覧表示コンポーネント
- `TransactionForm.vue` - 収入・支出登録フォームコンポーネント
- `ReportChart.vue` - レポートグラフ表示コンポーネント

## デプロイメント

### インフラ構築

- EC2 インスタンスのセットアップ
- RDS インスタンスのセットアップ
- S3 バケットの作成

### デプロイ手順

1. コードのリポジトリ（GitHub など）を設定
2. EC2 インスタンスにフロントエンドおよびバックエンドアプリケーションをデプロイ
3. RDS にデータベーススキーマを適用
4. S3 に静的ファイルをアップロード
5. ドメイン設定と SSL 証明書の適用（必要に応じて）

## タイムライン

- フロントエンド開発（3 時間）
- バックエンド開発（3 時間）
- データベース設計およびセットアップ（2 時間）
- デプロイおよびテスト（2 時間）
