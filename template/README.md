# {{ project_name }}

{{ project_description }}

## 概要

このプロジェクトは、Claude Code / GitHub Copilot を活用したAI駆動開発に最適化されたSaaSアプリケーションです。

## 技術スタック

| カテゴリ | 技術 |
|---------|------|
| フロントエンド | Next.js (TypeScript) |
| バックエンド | FastAPI (Python) |
| データベース | PostgreSQL |
| ORM | SQLAlchemy |
| マイグレーション | Alembic |
{%- if _enable_aws_auth %}
| 認証 | AWS Cognito / モックadapter |
{%- else %}
| 認証 | モックadapter |
{%- endif %}
{%- if _enable_aws_infra %}
| IaC | AWS CDK |
{%- endif %}

## クイックスタート

### 前提条件

- Docker & Docker Compose
- Node.js 20+
- pnpm
- Python 3.12+
- uv

### 初期セットアップ

```bash
# 依存関係のインストール（ロックファイル生成）
make setup

# または個別に実行
cd backend && uv sync --dev && cd ..
cd frontend && pnpm install && cd ..
```

### 開発環境の起動

```bash
# 全サービスを起動（マイグレーション含む）
make dev

# ログを確認
docker compose logs -f
```

> **Note**: `make dev` はコンテナ起動後に自動でデータベースマイグレーションを実行します。
> `docker compose up -d` を直接使用する場合は、別途 `make backend-migrate` の実行が必要です。

アプリケーションにアクセス:
- フロントエンド: http://localhost:3000
- バックエンドAPI: http://localhost:8000
- API ドキュメント (Swagger UI): http://localhost:8000/docs

### テストユーザー（ローカル開発）

ローカル開発環境ではモック認証が有効です。以下のテストユーザーでログインできます:

| メールアドレス | パスワード |
|---------------|-----------|
| test@example.com | password |

### ローカル開発（コンテナ外）

#### フロントエンド

```bash
cd frontend
pnpm install
pnpm dev
```

#### バックエンド

```bash
cd backend
uv sync
uv run uvicorn src.main:app --reload
```

## プロジェクト構造

```
.
├── frontend/          # Next.js アプリケーション
├── backend/           # FastAPI アプリケーション
{%- if _enable_aws_infra %}
├── infrastructure/    # AWS CDK
{%- endif %}
├── docs/              # ドキュメント
├── plans/             # 計画書
└── .github/           # GitHub設定（CI/CD, テンプレート）
```

## 開発ワークフロー

### ブランチ戦略

```
main        ← 本番リリース用
  ↑ PR
develop     ← 開発統合ブランチ
  ↑ PR
feature/*   ← 機能開発ブランチ
```

### AI駆動開発

このプロジェクトはAI駆動開発に最適化されています。

- **Claude Code**: `CLAUDE.md` と `AGENTS.md` を参照
- **GitHub Copilot**: `.github/copilot-instructions.md` を参照

### Issueからの開発フロー

1. GitHub Issueで機能追加/バグFIX/リファクタリングを起票
2. `plans/` に計画書を作成
3. 実装
4. テスト
5. ドキュメント更新
6. PR作成

## 開発コマンド（Makefile）

```bash
make help           # 利用可能なコマンド一覧
make setup          # 初期セットアップ
make dev            # 開発環境起動（マイグレーション含む）
make down           # 開発環境停止
make test           # 全テスト実行
make lint           # リンター実行
make format         # フォーマット実行
make clean          # クリーンアップ

# バックエンド
make backend-test   # バックエンドテスト
make backend-lint   # バックエンドリンター
make backend-migrate # マイグレーション実行

# フロントエンド
make frontend-test  # フロントエンドテスト
make frontend-lint  # フロントエンドリンター
{%- if _enable_e2e %}
make frontend-e2e   # E2Eテスト
{%- endif %}
```

## テスト

### フロントエンド

```bash
cd frontend
pnpm test          # ユニットテスト
{%- if _enable_e2e %}
pnpm e2e           # E2Eテスト
{%- endif %}
```

### バックエンド

```bash
cd backend
uv run pytest
```

## ドキュメント
{% if _enable_extended_docs %}
- [フロントエンド](./docs/frontend/README.md)
- [バックエンド](./docs/backend/README.md)
{%- if _enable_aws_infra %}
- [インフラ](./docs/infrastructure/README.md)
{%- endif %}
- [運用](./docs/operations/README.md)
{%- else %}
ドキュメントは `docs/` ディレクトリを参照してください。
{%- endif %}

## ライセンス

MIT
