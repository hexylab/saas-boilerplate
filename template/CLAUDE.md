# CLAUDE.md - Claude Code コンテキスト

このファイルはClaude Codeがプロジェクトを理解するためのコンテキストを提供します。

## プロジェクト概要

{{ project_name }} は、AI駆動開発に最適化されたSaaSアプリケーションです。

### 技術スタック

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

### パッケージマネージャー

- フロントエンド: pnpm
- バックエンド: uv

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
docker compose up -d
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

## コーディング規約

### フロントエンド (TypeScript/React)

- ESLint + Prettier の設定に従う
- コンポーネントは関数コンポーネント + フックを使用
- 状態管理: サーバー状態は React Query、クライアント状態は Zustand
- パスエイリアス: `@/` は `src/` を指す

### バックエンド (Python/FastAPI)

- Ruff の設定に従う（フォーマット + リント）
- mypy による型チェック必須
- docstring は Google スタイル
- 依存性注入は FastAPI の `Depends` を使用
- 外部サービスは adapters/ で抽象化

### 共通

- コミットメッセージは日本語可
- ブランチ名: `feature/`, `fix/`, `refactor/` プレフィックス

## API設計

- RESTful API
- バージョニング: `/api/v1/`
- 認証: Bearer トークン (JWT)
- エラーレスポンス: RFC 7807 Problem Details

## テスト方針

- ユニットテスト: ビジネスロジックを中心に
{%- if include_e2e_tests %}
- E2Eテスト: 主要なユーザーフローをカバー
{%- endif %}
- モック: 外部サービス（認証{%- if include_storage_adapter %}、ストレージ{%- endif %}）は adapters のモック実装を使用

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
