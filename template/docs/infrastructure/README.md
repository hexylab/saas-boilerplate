# インフラストラクチャ ドキュメント

## 概要

AWS CDK を使用したインフラストラクチャ as Code (IaC) です。

## 技術スタック

| カテゴリ | 技術 |
|---------|------|
| IaC | AWS CDK (TypeScript) |
| 認証 | Amazon Cognito |
| データベース | Amazon RDS (PostgreSQL) |
| ネットワーク | Amazon VPC |

## ディレクトリ構造

```
infrastructure/
├── bin/
│   └── app.ts               # CDKアプリケーションエントリポイント
├── lib/
│   ├── cognito-stack.ts     # Cognito User Pool
│   ├── database-stack.ts    # RDS PostgreSQL
│   └── network-stack.ts     # VPC設定
├── package.json
├── tsconfig.json
└── cdk.json
```

## 前提条件

- AWS CLI がインストール・設定されていること
- AWS アカウントへのアクセス権限があること
- Node.js 20+ がインストールされていること

## セットアップ

```bash
cd infrastructure

# 依存関係のインストール
npm install

# AWS CDK CLI のインストール（グローバル）
npm install -g aws-cdk

# CDK Bootstrap（初回のみ）
cdk bootstrap aws://ACCOUNT-NUMBER/REGION
```

## コマンド

```bash
# スタック一覧
cdk list

# 差分確認
cdk diff

# デプロイ
cdk deploy --all

# 特定のスタックをデプロイ
cdk deploy NetworkStack

# スタック削除
cdk destroy --all

# CloudFormation テンプレート生成
cdk synth
```

## スタック構成

### NetworkStack

VPC とネットワーク関連のリソースを管理します。

- VPC
- パブリック/プライベートサブネット
- NAT Gateway
- Security Groups

### DatabaseStack

RDS PostgreSQL を管理します。

- RDS インスタンス
- Secrets Manager（認証情報）
- サブネットグループ

### CognitoStack

認証基盤を管理します。

- User Pool
- User Pool Client
- Identity Pool（オプション）

## 環境変数

CDK デプロイ時に以下の環境変数を設定できます:

| 変数名 | 説明 | デフォルト |
|--------|------|----------|
| `CDK_DEFAULT_ACCOUNT` | AWSアカウントID | - |
| `CDK_DEFAULT_REGION` | AWSリージョン | `ap-northeast-1` |
| `ENVIRONMENT` | 環境名 (`dev` / `staging` / `prod`) | `dev` |

## コスト考慮事項

開発環境では以下の設定でコストを抑えることを推奨:

- RDS: `db.t3.micro` インスタンス
- NAT Gateway: 1つのみ（本番では各AZに配置）
- マルチAZ: 無効

## セキュリティ

- RDS はプライベートサブネットに配置
- Security Group で最小限のアクセスのみ許可
- Secrets Manager で認証情報を管理
- IAM ロールで最小権限の原則を適用
