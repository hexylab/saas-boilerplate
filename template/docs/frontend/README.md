# フロントエンド ドキュメント

## 概要

Next.js 14+ (App Router) を使用したフロントエンドアプリケーションです。

## 技術スタック

| カテゴリ | 技術 |
|---------|------|
| フレームワーク | Next.js 14+ (App Router) |
| 言語 | TypeScript |
| 状態管理 | React Query (サーバー状態) / Zustand (クライアント状態) |
| スタイリング | Tailwind CSS |
| テスト | Jest (ユニット) / Playwright (E2E) |
| リント | ESLint |
| フォーマット | Prettier |
| パッケージ管理 | pnpm |

## ディレクトリ構造

```
frontend/
├── src/
│   ├── app/                 # App Router ページ
│   │   ├── layout.tsx       # ルートレイアウト
│   │   ├── page.tsx         # ホーム/ログインページ
│   │   └── dashboard/       # ダッシュボード
│   │       └── page.tsx
│   ├── components/          # Reactコンポーネント
│   │   ├── ui/              # 汎用UIコンポーネント
│   │   └── features/        # 機能別コンポーネント
│   ├── lib/                 # ユーティリティ
│   │   ├── api.ts           # APIクライアント
│   │   └── auth.ts          # 認証ユーティリティ
│   ├── hooks/               # カスタムフック
│   ├── stores/              # Zustandストア
│   └── types/               # 型定義
├── tests/                   # Jestユニットテスト
├── e2e/                     # PlaywrightE2Eテスト
└── public/                  # 静的ファイル
```

## 開発コマンド

```bash
# 依存関係のインストール
pnpm install

# 開発サーバー起動
pnpm dev

# ビルド
pnpm build

# 本番サーバー起動
pnpm start

# リント
pnpm lint

# フォーマット
pnpm format

# フォーマットチェック
pnpm format:check

# ユニットテスト
pnpm test

# ユニットテスト（カバレッジ付き）
pnpm test --coverage

# E2Eテスト
pnpm test:e2e

# E2Eテスト（UIモード）
pnpm test:e2e:ui
```

## 環境変数

| 変数名 | 説明 | デフォルト |
|--------|------|----------|
| `NEXT_PUBLIC_API_URL` | バックエンドAPIのURL | `http://localhost:8000` |

## コーディング規約

### コンポーネント

- 関数コンポーネントを使用
- Props は interface で定義
- ファイル名は PascalCase

```typescript
interface ButtonProps {
  label: string;
  onClick: () => void;
}

export function Button({ label, onClick }: ButtonProps) {
  return <button onClick={onClick}>{label}</button>;
}
```

### パスエイリアス

`@/` は `src/` を指します。

```typescript
import { Button } from '@/components/ui/Button';
import { useAuth } from '@/hooks/useAuth';
```

### 状態管理

- **サーバー状態**: React Query を使用
- **クライアント状態**: Zustand を使用（必要な場合のみ）

## テスト

### ユニットテスト (Jest)

```typescript
import { render, screen } from '@testing-library/react';
import { Button } from '@/components/ui/Button';

describe('Button', () => {
  it('renders correctly', () => {
    render(<Button label="Click me" onClick={() => {}} />);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });
});
```

### E2Eテスト (Playwright)

```typescript
import { test, expect } from '@playwright/test';

test('login flow', async ({ page }) => {
  await page.goto('/');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('/dashboard');
});
```
