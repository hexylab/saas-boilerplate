# AI駆動開発向け SaaS ボイラープレート

Claude Code / GitHub Copilot を活用したAI駆動開発に最適化されたSaaSアプリケーションのボイラープレートテンプレートです。

## 特徴

- **軽量なベース構成**: 必要最小限のWalking Skeleton（ログイン → ダッシュボード）
- **プリセット選択**: minimal / standard / aws の3つのプリセットから選択
- **AI駆動開発対応**: CLAUDE.md, AGENTS.md, copilot-instructions.md 完備
- **フルスタック**: Next.js (TypeScript) + FastAPI (Python) + PostgreSQL
- **CI/CD**: GitHub Actions (lint, test, build, セキュリティ/監査)
- **Copier対応**: プロジェクト名等をカスタマイズして生成

## 技術スタック

| カテゴリ | 技術 |
|---------|------|
| フロントエンド | Next.js 14+ (App Router), TypeScript, Tailwind CSS |
| 状態管理 | React Query (サーバー), Zustand (クライアント) |
| バックエンド | FastAPI, Python 3.12+, SQLAlchemy 2.0 (async) |
| データベース | PostgreSQL 16 |
| マイグレーション | Alembic |
| 認証 | モック認証（ベース）/ AWS Cognito（オプション） |
| IaC | AWS CDK（オプション） |
| パッケージ管理 | pnpm (frontend), uv (backend) |
| Linter/Formatter | ESLint + Prettier, Ruff + mypy |
| テスト | Jest + pytest（ベース）/ Playwright E2E（オプション） |

## 使用方法

### 前提条件

- [Copier](https://copier.readthedocs.io/) 9.0.0+
- Docker & Docker Compose
- Node.js 20+, pnpm
- Python 3.12+, uv

### 1. Copierのインストール

```bash
# pipx を使用（推奨）
pipx install copier

# または pip
pip install copier
```

### 2. テンプレートからプロジェクトを生成

```bash
# このリポジトリをクローン
git clone https://github.com/hexylab/saas-boilerplate.git

# Copierでプロジェクトを生成
copier copy ./saas-boilerplate ~/my-project

# または直接GitHubから
copier copy gh:hexylab/saas-boilerplate ~/my-project
```

### 3. 対話形式で設定

```
? プロジェクト名（例: My SaaS App） My Awesome App
? プロジェクトスラッグ my-awesome-app
? プロジェクトの説明 AI駆動開発に最適化されたSaaSアプリケーション
? 使用するAI Codingエージェント both
? プリセットを選択してください standard
```

※ `aws` プリセットを選択した場合のみ、AWSリージョンの選択が表示されます。

### 4. 生成されたプロジェクトをセットアップ

```bash
cd ~/my-project

# 依存関係のインストール
make setup

# 開発環境の起動（マイグレーション含む）
make dev

# アクセス
# フロントエンド: http://localhost:3000
# バックエンド:   http://localhost:8000/docs
```

> **Note**: `make dev` はコンテナ起動後に自動でデータベースマイグレーションを実行します。

### テストユーザー（ローカル開発）

| メールアドレス | パスワード |
|---------------|-----------|
| test@example.com | password |

## ディレクトリ構成

```
saas-boilerplate/
├── copier.yml              # Copier設定（テンプレート変数定義）
├── README.md               # このファイル
└── template/               # テンプレート本体
    ├── CLAUDE.md           # Claude Code用コンテキスト
    ├── AGENTS.md           # エージェント共通ガイド
    ├── README.md           # 生成プロジェクト用README
    ├── Makefile            # 開発コマンド
    ├── docker-compose.yml  # フルスタック起動
    ├── .github/            # CI/CD, Issue/PRテンプレート
    ├── frontend/           # Next.js アプリケーション
    ├── backend/            # FastAPI アプリケーション
    ├── infrastructure/     # AWS CDK
    ├── docs/               # ドキュメント
    └── plans/              # 計画書置き場
```

## テンプレート変数

### 基本設定

| 変数名 | 説明 | デフォルト |
|--------|------|-----------|
| `project_name` | プロジェクト名 | (必須) |
| `project_slug` | スラッグ（ディレクトリ名等） | project_name から自動生成 |
| `project_description` | プロジェクトの説明 | AI駆動開発に最適化された... |
| `ai_coding_agent` | AI Codingエージェント選択 | both |
| `preset` | プリセット選択 | standard |
| `aws_region` | AWSリージョン（awsプリセット時のみ） | ap-northeast-1 |

### プリセット

| プリセット | 対象 | 含まれる機能 |
|------------|------|-------------|
| `minimal` | 学習・PoC | ベース構成のみ |
| `standard` | チーム開発 | E2E + PRチェック + セキュリティ/監査 + 詳細ドキュメント |
| `aws` | AWS本番環境 | standard + Cognito認証 + S3ストレージ + CDK |

**ベース構成（常に含まれる）:**
- Next.js フロントエンド（ログイン + ダッシュボード）
- FastAPI バックエンド（モック認証 + ローカルストレージ）
- Docker Compose 開発環境
- GitHub Actions CI（lint, test, build）
- CLAUDE.md / copilot-instructions.md

**standard/awsで追加:**
- Playwright E2Eテスト
- PRチェックワークフロー（labeler）
- セキュリティ/監査ワークフロー（Gitleaks, Trivy, pip-audit, npm audit, ライセンスチェック）
- カバレッジレポート（PRコメント）
- 詳細ドキュメント構造

**awsで追加:**
- AWS Cognito認証アダプター
- S3ストレージアダプター
- AWS CDKインフラ

## テンプレートの更新

プロジェクト生成後、テンプレートの更新を適用するには:

```bash
cd ~/my-project
copier update
```

## 開発ワークフロー

生成されたプロジェクトでは、以下のIssue駆動開発フローを推奨します:

1. **Issue作成**: 機能追加/バグ修正/リファクタリング
2. **計画**: `plans/` に計画書を作成
3. **実装**: feature/* ブランチで開発
4. **テスト**: `make test` で検証
5. **ドキュメント**: `docs/` を更新
6. **PR**: develop → main

## ライセンス

MIT
