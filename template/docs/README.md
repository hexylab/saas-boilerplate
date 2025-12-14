# {{ project_name }} ドキュメント

## 概要

このディレクトリにはプロジェクトのドキュメントを配置します。

## ドキュメント構成
{% if include_extended_docs %}
- [フロントエンド](./frontend/README.md) - Next.js アプリケーション
- [バックエンド](./backend/README.md) - FastAPI アプリケーション
{%- if include_infrastructure %}
- [インフラ](./infrastructure/README.md) - AWS CDK
{%- endif %}
- [運用](./operations/README.md) - 運用関連ドキュメント
{%- else %}
ドキュメントを追加する場合は、以下のような構成を推奨します:

```
docs/
├── README.md          # このファイル
├── architecture.md    # アーキテクチャ設計
├── api.md             # API仕様
└── deployment.md      # デプロイ手順
```
{%- endif %}

## クイックリンク

- [プロジェクトREADME](../README.md)
- [CLAUDE.md](../CLAUDE.md) - Claude Code用コンテキスト
- [計画書](../plans/) - 機能追加・バグ修正の計画書
