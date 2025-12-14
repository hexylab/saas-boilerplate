# AGENTS.md - AI Coding エージェント共通ガイド

このファイルは、Claude Code、GitHub Copilot、その他のAI Codingエージェントが共通して参照するガイドラインです。

## プロジェクト情報

- **プロジェクト名**: {{ project_name }}
- **説明**: {{ project_description }}
- **作者**: {{ author_name }}

## 開発ワークフロー

### Issue駆動開発

1. **Issue作成**: GitHub Issueで作業内容を定義
2. **計画策定**: `plans/` に計画書を作成
3. **実装**: コードを書く
{% if include_e2e_tests %}
4. **テスト**: ユニットテスト・E2Eテストを実行
{% else %}
4. **テスト**: ユニットテストを実行
{% endif %}
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
{% if include_extended_docs %}
| ドキュメント | `docs/{frontend,backend{% if include_infrastructure %},infrastructure{% endif %},operations}/` |
{% else %}
| ドキュメント | `docs/` |
{% endif %}

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
