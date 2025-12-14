# AGENTS.md - AI Coding エージェント共通ガイド

このファイルは、Claude Code、GitHub Copilot、その他のAI Codingエージェントが共通して参照するガイドラインです。

## プロジェクト情報

- **プロジェクト名**: {{ project_name }}
- **説明**: {{ project_description }}
- **作者**: {{ author_name }}

## 技術スタック

- **フロントエンド**: Next.js 14+ (App Router, TypeScript)
- **バックエンド**: FastAPI (Python 3.12+)
- **データベース**: PostgreSQL 16
- **ORM**: SQLAlchemy 2.0 + Alembic
{%- if include_advanced_auth %}
- **認証**: AWS Cognito / モックadapter
{%- else %}
- **認証**: モックadapter（ローカル開発用）
{%- endif %}
{%- if include_infrastructure %}
- **IaC**: AWS CDK
{%- endif %}
- **パッケージ管理**: pnpm (frontend), uv (backend)

## ディレクトリ構造

```
.
├── frontend/          # Next.js アプリケーション
│   ├── src/
│   │   ├── app/       # App Router ページ
│   │   ├── components/ # React コンポーネント
│   │   ├── lib/       # ユーティリティ、APIクライアント
│   │   ├── hooks/     # カスタムフック
│   │   ├── stores/    # Zustand ストア
│   │   └── types/     # TypeScript 型定義
│   └── tests/         # テスト
│       ├── components/ # Jest ユニットテスト
{%- if include_e2e_tests %}
│       └── e2e/        # Playwright E2Eテスト
{%- endif %}
│
├── backend/           # FastAPI アプリケーション
│   ├── src/
│   │   ├── adapters/  # 外部サービス抽象化（認証{%- if include_storage_adapter %}、ストレージ{%- endif %}）
│   │   ├── api/       # APIエンドポイント
│   │   ├── core/      # 共通機能（ログ、セキュリティ）
│   │   ├── db/        # データベース設定
│   │   ├── models/    # SQLAlchemy モデル
│   │   └── schemas/   # Pydantic スキーマ
│   └── tests/         # pytest テスト
│
{%- if include_infrastructure %}
├── infrastructure/    # AWS CDK スタック
{%- endif %}
├── docs/              # ドキュメント
└── plans/             # 計画書
```

## 開発コマンド

### 全サービス起動

```bash
# 推奨: マイグレーション含む
make dev

# または docker compose のみ（マイグレーションは別途実行）
docker compose up -d
docker compose exec backend uv run alembic upgrade head
```

### フロントエンド

```bash
cd frontend
pnpm dev          # 開発サーバー
pnpm build        # ビルド
pnpm test         # ユニットテスト
{%- if include_e2e_tests %}
pnpm e2e          # E2Eテスト
{%- endif %}
pnpm lint         # ESLint
pnpm format       # Prettier
```

### バックエンド

```bash
cd backend
uv run uvicorn src.main:app --reload  # 開発サーバー
uv run pytest                          # テスト
uv run ruff check .                    # リント
uv run ruff format .                   # フォーマット
uv run mypy src                        # 型チェック
```

### データベースマイグレーション

```bash
cd backend
uv run alembic upgrade head            # マイグレーション適用
uv run alembic revision --autogenerate -m "message"  # マイグレーション作成
```

## 開発ワークフロー

### Issue駆動開発

1. **Issue作成**: GitHub Issueで作業内容を定義
2. **計画策定**: `plans/` に計画書を作成
3. **実装**: コードを書く
{%- if include_e2e_tests %}
4. **テスト**: ユニットテスト・E2Eテストを実行
{%- else %}
4. **テスト**: ユニットテストを実行
{%- endif %}
5. **ドキュメント**: 必要に応じてdocs/を更新
6. **PR作成**: developブランチへPRを作成

### ブランチ戦略

```
main        ← 本番用（protectedブランチ）
  ↑
develop     ← 開発統合ブランチ（protectedブランチ）
  ↑
feature/*   ← 機能開発
fix/*       ← バグ修正
refactor/*  ← リファクタリング
```

## ファイル配置ルール

### 新しいファイルを作成する場合

| 種類 | 配置場所 |
|------|----------|
| Reactコンポーネント | `frontend/src/components/` |
| ページ | `frontend/src/app/` |
| カスタムフック | `frontend/src/hooks/` |
| 型定義 | `frontend/src/types/` |
| APIエンドポイント | `backend/src/api/v1/` |
| データモデル | `backend/src/models/` |
| Pydanticスキーマ | `backend/src/schemas/` |
| 外部サービス連携 | `backend/src/adapters/` |
| 計画書 | `plans/` |
{%- if include_extended_docs %}
| ドキュメント | `docs/{frontend,backend{%- if include_infrastructure %},infrastructure{%- endif %},operations}/` |
{%- else %}
| ドキュメント | `docs/` |
{%- endif %}

## コード生成のガイドライン

### フロントエンド (TypeScript/React)

```typescript
// コンポーネントは関数コンポーネントで記述
export function MyComponent({ prop }: MyComponentProps) {
  return <div>{prop}</div>;
}

// 型は明示的に定義
interface MyComponentProps {
  prop: string;
}

// APIコールはReact Queryを使用
const { data, isLoading } = useQuery({
  queryKey: ['resource'],
  queryFn: () => api.getResource(),
});
```

### バックエンド (Python/FastAPI)

```python
"""モジュールのdocstring - Google スタイル."""

from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/resource")
async def get_resource(
    service: ResourceService = Depends(get_resource_service),
) -> ResourceResponse:
    """リソースを取得する.

    Args:
        service: リソースサービス

    Returns:
        リソースのレスポンス
    """
    return await service.get()
```

## エラーハンドリング

### フロントエンド

- React Query の `onError` コールバックを使用
- ユーザーにはトースト通知で表示
- エラー境界でクラッシュを防止

### バックエンド

- カスタム例外クラスを定義
- 例外ハンドラーで適切なHTTPレスポンスに変換
- RFC 7807 Problem Details 形式

```python
# エラーレスポンス例
{
    "type": "https://example.com/errors/not-found",
    "title": "Resource Not Found",
    "status": 404,
    "detail": "The requested resource was not found."
}
```

## テスト記述

### フロントエンド (Jest)

```typescript
describe('MyComponent', () => {
  it('should render correctly', () => {
    render(<MyComponent prop="test" />);
    expect(screen.getByText('test')).toBeInTheDocument();
  });
});
```

### バックエンド (pytest)

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_resource(client: AsyncClient):
    """リソース取得のテスト."""
    response = await client.get("/api/v1/resource")
    assert response.status_code == 200
```

## セキュリティ考慮事項

- 環境変数で機密情報を管理（.env ファイルはコミットしない）
- SQLインジェクション対策: SQLAlchemy のパラメータバインディングを使用
- XSS対策: Reactのデフォルトエスケープを活用
- CSRF対策: 適切なCORS設定
- 認証: JWT トークンの適切な検証

## 禁止事項

- `.env` ファイルのコミット
- ハードコードされた機密情報
- `console.log` / `print` のコミット（デバッグ用途）
- テストなしでのPRマージ
- main/developブランチへの直接プッシュ

## 計画書の作成

機能追加・バグFIX・リファクタリングを行う際は、`plans/` ディレクトリに計画書を作成してください。

```markdown
# 計画書テンプレート

## 概要
何を実現するか

## 背景
なぜ必要か

## 設計
どのように実現するか

## 影響範囲
どのファイルを変更するか

## テスト計画
どのようにテストするか
```
