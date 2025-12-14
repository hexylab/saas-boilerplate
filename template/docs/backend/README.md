# バックエンド ドキュメント

## 概要

FastAPI を使用したバックエンドAPIアプリケーションです。

## 技術スタック

| カテゴリ | 技術 |
|---------|------|
| フレームワーク | FastAPI |
| 言語 | Python 3.12+ |
| ORM | SQLAlchemy 2.0 (async) |
| マイグレーション | Alembic |
| バリデーション | Pydantic v2 |
| テスト | pytest |
| リント/フォーマット | Ruff |
| 型チェック | mypy |
| パッケージ管理 | uv |

## ディレクトリ構造

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py              # アプリケーションエントリポイント
│   ├── config.py            # 設定管理
│   ├── adapters/            # 外部サービス抽象化
│   │   ├── auth/            # 認証adapter
│   │   │   ├── base.py      # AuthProvider ABC
│   │   │   ├── cognito.py   # AWS Cognito実装
│   │   │   └── mock.py      # モック実装
│   │   └── storage/         # ストレージadapter
│   │       ├── base.py      # StorageProvider ABC
│   │       ├── s3.py        # AWS S3実装
│   │       └── local.py     # ローカル実装
│   ├── api/                 # APIエンドポイント
│   │   ├── router.py        # メインルーター
│   │   ├── deps.py          # 依存性注入
│   │   └── v1/              # APIバージョン1
│   │       ├── auth.py      # 認証エンドポイント
│   │       └── users.py     # ユーザーエンドポイント
│   ├── core/                # 共通機能
│   │   ├── logging.py       # ログ設定
│   │   └── security.py      # セキュリティ
│   ├── db/                  # データベース
│   │   ├── session.py       # セッション管理
│   │   └── base.py          # ベースモデル
│   ├── models/              # SQLAlchemyモデル
│   │   └── user.py
│   └── schemas/             # Pydanticスキーマ
│       └── user.py
├── tests/                   # テスト
├── alembic/                 # マイグレーション
└── storage/                 # ローカルストレージ
```

## 開発コマンド

```bash
# 依存関係のインストール
uv sync

# 開発サーバー起動
uv run uvicorn src.main:app --reload

# リント
uv run ruff check .

# リント（自動修正）
uv run ruff check --fix .

# フォーマット
uv run ruff format .

# フォーマットチェック
uv run ruff format --check .

# 型チェック
uv run mypy src

# テスト
uv run pytest

# テスト（カバレッジ付き）
uv run pytest --cov=src --cov-report=html
```

## データベースマイグレーション

```bash
# マイグレーション適用
uv run alembic upgrade head

# マイグレーション作成（自動生成）
uv run alembic revision --autogenerate -m "Add users table"

# マイグレーション履歴確認
uv run alembic history

# 1つ前に戻す
uv run alembic downgrade -1
```

## 環境変数

| 変数名 | 説明 | デフォルト |
|--------|------|----------|
| `DATABASE_URL` | データベース接続URL | - |
| `SECRET_KEY` | JWT署名用シークレット | - |
| `AUTH_PROVIDER` | 認証プロバイダー (`mock` / `cognito`) | `mock` |
| `STORAGE_PROVIDER` | ストレージプロバイダー (`local` / `s3`) | `local` |
| `LOG_HANDLER` | ログハンドラー (`console` / `cloudwatch`) | `console` |
| `CORS_ORIGINS` | 許可するオリジン（カンマ区切り） | - |

## APIドキュメント

開発サーバー起動後、以下のURLでAPIドキュメントにアクセスできます:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## コーディング規約

### docstring

Google スタイルを使用します。

```python
def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """ユーザーをIDで取得する.

    Args:
        db: データベースセッション
        user_id: ユーザーID

    Returns:
        ユーザーオブジェクト。見つからない場合はNone。

    Raises:
        DatabaseError: データベースエラーが発生した場合
    """
```

### 依存性注入

FastAPI の `Depends` を使用します。

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.adapters.auth import get_auth_provider

@router.get("/users/me")
async def get_current_user(
    db: AsyncSession = Depends(get_db),
    auth: AuthProvider = Depends(get_auth_provider),
):
    ...
```

### Adapter パターン

外部サービスは adapter で抽象化し、環境変数で切り替え可能にします。

```python
# src/adapters/auth/base.py
from abc import ABC, abstractmethod

class AuthProvider(ABC):
    @abstractmethod
    async def verify_token(self, token: str) -> dict:
        """トークンを検証する."""
        pass
```

## テスト

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_user(client: AsyncClient, auth_headers: dict):
    """ユーザー取得のテスト."""
    response = await client.get("/api/v1/users/me", headers=auth_headers)
    assert response.status_code == 200
    assert "email" in response.json()
```
