# {{ project_name }} Backend

FastAPI バックエンドアプリケーション

## セットアップ

```bash
# 依存関係のインストール
uv sync --dev

# 開発サーバー起動
uv run uvicorn src.main:app --reload
```

## 開発コマンド

```bash
# テスト
uv run pytest

# リント
uv run ruff check .

# フォーマット
uv run ruff format .

# 型チェック
uv run mypy src

# マイグレーション
uv run alembic upgrade head
```

## API ドキュメント

開発サーバー起動後、以下のURLでAPIドキュメントを確認できます:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
