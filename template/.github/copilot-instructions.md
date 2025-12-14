# GitHub Copilot Instructions

このファイルはGitHub Copilotに対するプロジェクト固有の指示を提供します。

## プロジェクト概要

{{ project_name }} は Next.js + FastAPI で構成されたSaaSアプリケーションです。

## 技術スタック

### フロントエンド
- Next.js 14+ (App Router)
- TypeScript (strict mode)
- React Query (TanStack Query) - サーバー状態管理
- Zustand - クライアント状態管理
- ESLint + Prettier

### バックエンド
- FastAPI
- Python 3.12+
- SQLAlchemy 2.0 (async)
- Pydantic v2
- Ruff + mypy

## コーディングスタイル

### TypeScript/React

- 関数コンポーネントを使用
- Props は interface で定義
- パスエイリアス `@/` を使用 (`@/components/`, `@/lib/` など)
- 非同期処理は async/await を使用

```typescript
// 推奨するコンポーネントスタイル
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
}

export function Button({ label, onClick, variant = 'primary' }: ButtonProps) {
  return (
    <button onClick={onClick} className={`btn btn-${variant}`}>
      {label}
    </button>
  );
}
```

### Python/FastAPI

- Google スタイルの docstring
- 型アノテーション必須
- async def を使用（同期処理が必要な場合のみ def）
- 依存性注入は Depends を使用

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """ユーザーを取得する.

    Args:
        user_id: ユーザーID
        db: データベースセッション

    Returns:
        ユーザー情報

    Raises:
        HTTPException: ユーザーが見つからない場合
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

## ファイル配置

新しいファイルを作成する際は以下のルールに従ってください:

- React コンポーネント: `frontend/src/components/{feature}/`
- ページ: `frontend/src/app/`
- カスタムフック: `frontend/src/hooks/`
- API エンドポイント: `backend/src/api/v1/`
- データモデル: `backend/src/models/`
- Pydantic スキーマ: `backend/src/schemas/`

## インポート順序

### TypeScript

```typescript
// 1. React/Next.js
import { useState } from 'react';
import { useRouter } from 'next/navigation';

// 2. 外部ライブラリ
import { useQuery } from '@tanstack/react-query';

// 3. 内部モジュール（エイリアス使用）
import { Button } from '@/components/ui/Button';
import { api } from '@/lib/api';
import type { User } from '@/types';
```

### Python

```python
# 1. 標準ライブラリ
from datetime import datetime
from typing import Optional

# 2. サードパーティ
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# 3. ローカル
from src.core.logging import logger
from src.models.user import User
```

## 命名規則

| 種類 | スタイル | 例 |
|------|---------|-----|
| TypeScript 変数/関数 | camelCase | `getUserById` |
| TypeScript 型/interface | PascalCase | `UserResponse` |
| React コンポーネント | PascalCase | `UserProfile` |
| Python 変数/関数 | snake_case | `get_user_by_id` |
| Python クラス | PascalCase | `UserService` |
| 定数 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |

## 避けるべきパターン

- `any` 型の使用（TypeScript）
- `# type: ignore` コメント（Python）
- ハードコードされた文字列（環境変数を使用）
- console.log / print のコミット
- 未使用のインポート
