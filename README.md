# gameserver-pilot

ゲームサーバーをDiscordから操作し、プレイヤー不在時に自動停止するシステムです。

## 概要

このプロジェクトは、AWS EC2上のゲームサーバーをDiscordのスラッシュコマンドで起動・停止し、プレイヤーがいない状態が一定時間続くと自動的にサーバーを停止してコストを最適化します。

ゲームごとにプレイヤー数取得の実装を追加することで、様々なゲームサーバーに対応できます。

## 主な機能

- Discordスラッシュコマンドによるサーバー操作
  - `/start <server>` - サーバー起動
  - `/stop <server>` - サーバー停止
  - `/status <server>` - 状態確認

- プレイヤー数に基づく自動停止
  - 0人の状態が1時間継続で自動停止
  - ゲームごとのプレイヤー監視プラグイン

- AWS EC2連携
  - boto3によるインスタンス操作
  - 停止時はストレージのみ課金

## 対応ゲーム

| ゲーム | プレイヤー数取得方式 | 状態 |
|--------|---------------------|------|
| Terraria (TShock) | REST API | 予定 |
| Terraria (Vanilla) | ログファイル監視 | 予定 |
| Core Keeper | ログファイル監視 | 予定 |

## アーキテクチャ

```
┌─────────────────────────────────────────────────┐
│  Discord Bot (Railway)                          │
│  - スラッシュコマンド受付                          │
│  - boto3でEC2操作                               │
│  - 自動停止ロジック                              │
└─────────────────┬───────────────────────────────┘
                  │ AWS API
                  ▼
┌─────────────────────────────────────────────────┐
│  AWS EC2 (東京リージョン)                        │
│                                                 │
│  ┌─────────────┐  ┌─────────────┐              │
│  │ Terraria    │  │ Core Keeper │  ...         │
│  │ t3.small    │  │ t3.medium   │              │
│  └─────────────┘  └─────────────┘              │
└─────────────────────────────────────────────────┘
```

## プロジェクト構造

```text
gameserver-pilot/
├── gameserver_pilot/
│   ├── __init__.py
│   ├── bot.py                 # Discord Bot メイン
│   ├── cloud/                 # クラウドプロバイダー
│   │   ├── __init__.py
│   │   ├── base.py           # 抽象クラス
│   │   ├── ec2.py            # AWS EC2実装
│   │   └── mock.py           # 開発用モック
│   └── monitors/              # プレイヤー監視
│       ├── __init__.py
│       ├── base.py           # 抽象クラス
│       ├── tshock.py         # TShock REST API
│       └── logfile.py        # ログファイル監視
├── tests/
├── pyproject.toml
└── README.md
```

## セットアップ

### 前提条件

- Python 3.14以上
- AWS アカウント（EC2操作権限）
- Discord Bot Token

### インストール

```bash
git clone https://github.com/rysk-tanaka/gameserver-pilot.git
cd gameserver-pilot
uv sync
```

### 環境変数

```bash
# Discord
DISCORD_TOKEN="your-bot-token"

# AWS
AWS_ACCESS_KEY_ID="your-access-key"
AWS_SECRET_ACCESS_KEY="your-secret-key"
AWS_DEFAULT_REGION="ap-northeast-1"

# 開発時はモックを使用
ENV="development"  # or "production"
```

## 使い方

### ローカル実行

```bash
# 開発モード（モックEC2）
ENV=development uv run python -m gameserver_pilot.bot

# 本番モード
ENV=production uv run python -m gameserver_pilot.bot
```

### Discordコマンド

```
/start terraria     # Terrariaサーバーを起動
/stop terraria      # Terrariaサーバーを停止
/status terraria    # 状態を確認
```

## 開発

```bash
# フォーマット
uv run ruff format .

# リント
uv run ruff check .

# テスト
uv run pytest
```
