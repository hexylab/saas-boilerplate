# 運用 ドキュメント

## 概要

アプリケーションの運用に関するドキュメントです。

## 目次

- [ログ設定](./logging.md)

## ローカル開発環境

### 起動

```bash
# 全サービス起動
docker compose up -d

# ログ確認
docker compose logs -f

# 特定サービスのログ確認
docker compose logs -f backend
```

### 停止

```bash
# 全サービス停止
docker compose down

# ボリュームも含めて削除
docker compose down -v
```

### 再ビルド

```bash
# 特定サービスの再ビルド
docker compose build backend

# 再ビルドして起動
docker compose up -d --build
```

## 環境別設定

### 開発環境 (local)

- `AUTH_PROVIDER=mock` - モック認証を使用
- `STORAGE_PROVIDER=local` - ローカルファイルシステムを使用
- `LOG_HANDLER=console` - コンソールにログ出力

### ステージング環境 (staging)

- `AUTH_PROVIDER=cognito` - Cognito認証を使用
- `STORAGE_PROVIDER=s3` - S3を使用
- `LOG_HANDLER=cloudwatch` - CloudWatchにログ出力

### 本番環境 (production)

- `AUTH_PROVIDER=cognito` - Cognito認証を使用
- `STORAGE_PROVIDER=s3` - S3を使用
- `LOG_HANDLER=cloudwatch` - CloudWatchにログ出力

## ヘルスチェック

### バックエンド

```bash
curl http://localhost:8000/health
```

レスポンス例:
```json
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0"
}
```

### フロントエンド

```bash
curl http://localhost:3000/api/health
```

## トラブルシューティング

### データベース接続エラー

1. PostgreSQL が起動しているか確認
   ```bash
   docker compose ps db
   ```

2. 接続情報が正しいか確認
   ```bash
   docker compose exec backend env | grep DATABASE
   ```

3. マイグレーションが適用されているか確認
   ```bash
   docker compose exec backend uv run alembic current
   ```

### 認証エラー

1. 認証プロバイダーの設定を確認
   ```bash
   docker compose exec backend env | grep AUTH_PROVIDER
   ```

2. モック認証の場合、テストユーザーでログインできるか確認
   - Email: `test@example.com`
   - Password: `password`

### ログが出力されない

1. ログハンドラーの設定を確認
   ```bash
   docker compose exec backend env | grep LOG_HANDLER
   ```

2. ログレベルを確認
   ```bash
   docker compose exec backend env | grep LOG_LEVEL
   ```

## バックアップ

### データベース

```bash
# バックアップ作成
docker compose exec db pg_dump -U postgres app > backup.sql

# リストア
docker compose exec -T db psql -U postgres app < backup.sql
```

### ローカルストレージ

```bash
# バックアップ
tar -czf storage-backup.tar.gz backend/storage/

# リストア
tar -xzf storage-backup.tar.gz
```
