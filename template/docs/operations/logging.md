# ログ設定ガイド

## 概要

このプロジェクトでは、構造化ログ（JSON形式）を採用しています。
ログハンドラーは環境変数で切り替え可能です。

## 環境変数

| 変数名 | 説明 | 選択肢 | デフォルト |
|--------|------|--------|----------|
| `LOG_HANDLER` | ログ出力先 | `console`, `cloudwatch`, `datadog` | `console` |
| `LOG_LEVEL` | ログレベル | `DEBUG`, `INFO`, `WARNING`, `ERROR` | `INFO` |
| `LOG_FORMAT` | ログフォーマット | `json`, `text` | `json` |

## ログハンドラー

### console

開発環境向け。標準出力にログを出力します。

```bash
LOG_HANDLER=console
```

出力例（JSON形式）:
```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "level": "INFO",
  "message": "User logged in",
  "user_id": 123,
  "request_id": "abc-123"
}
```

### cloudwatch

AWS CloudWatch Logs にログを送信します。

```bash
LOG_HANDLER=cloudwatch
AWS_REGION=ap-northeast-1
CLOUDWATCH_LOG_GROUP=/app/backend
```

必要なIAMポリシー:
```json
{
  "Effect": "Allow",
  "Action": [
    "logs:CreateLogGroup",
    "logs:CreateLogStream",
    "logs:PutLogEvents"
  ],
  "Resource": "arn:aws:logs:*:*:*"
}
```

### datadog (将来対応)

Datadog にログを送信します。

```bash
LOG_HANDLER=datadog
DD_API_KEY=your-api-key
DD_SITE=datadoghq.com
```

## カスタムハンドラーの追加

新しいログハンドラーを追加する場合:

1. `backend/src/core/logging.py` にハンドラークラスを追加

```python
class CustomHandler:
    def emit(self, record: dict) -> None:
        # カスタムログ処理
        pass
```

2. `get_handler` 関数にケースを追加

```python
def get_handler(handler_type: str) -> Handler:
    handlers = {
        "console": ConsoleHandler,
        "cloudwatch": CloudWatchHandler,
        "custom": CustomHandler,  # 追加
    }
    return handlers[handler_type]()
```

## ログの使用方法

### バックエンド (Python)

```python
from src.core.logging import logger

# 基本的なログ
logger.info("User logged in", user_id=123)

# エラーログ（例外情報付き）
try:
    ...
except Exception as e:
    logger.exception("Failed to process request", error=str(e))

# リクエストコンテキスト付き
logger.info(
    "API request",
    method="GET",
    path="/api/v1/users",
    status_code=200,
    duration_ms=45,
)
```

### フロントエンド (TypeScript)

フロントエンドでは、開発時はコンソール、本番ではサーバーサイドにログを送信することを推奨します。

```typescript
// lib/logger.ts
const logger = {
  info: (message: string, data?: Record<string, unknown>) => {
    if (process.env.NODE_ENV === 'development') {
      console.log(JSON.stringify({ level: 'info', message, ...data }));
    } else {
      // 本番では API 経由でバックエンドに送信
      fetch('/api/log', {
        method: 'POST',
        body: JSON.stringify({ level: 'info', message, ...data }),
      });
    }
  },
};
```

## ログレベルガイドライン

| レベル | 用途 |
|--------|------|
| `DEBUG` | 開発時のデバッグ情報。本番では無効化 |
| `INFO` | 正常な動作の記録（ユーザーアクション、API呼び出しなど） |
| `WARNING` | 注意が必要だが処理は継続可能な状況 |
| `ERROR` | エラー発生。即座の対応が必要な場合もある |

## 機密情報の取り扱い

以下の情報はログに出力しないでください:

- パスワード
- アクセストークン
- APIキー
- クレジットカード情報
- 個人情報（必要な場合はマスキング）

```python
# NG
logger.info("Login", password=user.password)

# OK
logger.info("Login", user_id=user.id)
```
