# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

ゲームサーバーをDiscordから操作し、プレイヤー不在時に自動停止するシステム。
AWS EC2上のゲームサーバーをDiscordスラッシュコマンドで起動・停止し、プレイヤー0人が一定時間続くと自動停止する。

## 開発コマンド

```bash
# 依存関係のインストール
uv sync --group dev

# Bot起動（開発モード: MockProvider使用）
ENV=development uv run python -m gameserver_pilot.bot

# Bot起動（本番モード: EC2Provider使用）
ENV=production uv run python -m gameserver_pilot.bot

# テスト
uv run pytest
uv run pytest tests/cloud/test_ec2.py -v          # 単一ファイル
uv run pytest -k "test_start"                     # パターンマッチ
uv run pytest --cov=gameserver_pilot              # カバレッジ付き

# コード品質
uv run ruff format .
uv run ruff check .
uv run mypy gameserver_pilot
pyright gameserver_pilot tests
```

## アーキテクチャ

### 拡張ポイント（Strategy Pattern）

このプロジェクトは2つの抽象クラスによる拡張ポイントを持つ。

CloudProvider (`cloud/base.py`)

- クラウドプロバイダーの抽象化
- 実装: EC2Provider（本番）、MockProvider（開発）
- メソッド: `start_server()`, `stop_server()`, `get_server_status()`

PlayerMonitor (`monitors/base.py`)

- プレイヤー数取得の抽象化
- 実装: TShockMonitor（REST API）、LogFileMonitor（ログ監視）
- メソッド: `get_player_count()`

Monitoring (`monitoring/`)

- Beszel Hub との連携によるリソース監視
- BeszelClient: REST API クライアント
- MonitoringReporter: 定期レポート送信（discord.ext.tasks）

### 環境による切り替え

`ENV`環境変数でCloudProviderの実装を切り替える。

- `development`: MockProvider（EC2を操作しない）
- `production`: EC2Provider（実際のEC2を操作）

## コード規約

ruff設定 (pyproject.toml)

- 行長: 100文字
- 有効ルール: E, W, F, UP, B, I, C90, PLR
- 複雑度上限: 10

pytest設定

- `asyncio_mode = "auto"` により async テストは自動検出
- デフォルトでカバレッジレポート出力

テスト用モックライブラリ

- moto: AWS（EC2等）のモック
- respx: httpxのモック

テスト配置

- `tests/cloud/`: CloudProvider実装のテスト
- `tests/monitors/`: PlayerMonitor実装のテスト
- `tests/monitoring/`: Beszel連携のテスト

## 実装ガイドライン

新しいゲームを追加する場合

1. `monitors/`にPlayerMonitorを継承したクラスを作成
2. `get_player_count()`を実装
3. `tests/monitors/`にテストを追加

新しいクラウドプロバイダーを追加する場合

1. `cloud/`にCloudProviderを継承したクラスを作成
2. 全メソッドを実装
3. `tests/cloud/`にテストを追加

注意点

- すべてのI/O操作はasync/awaitを使用
- HTTP通信はhttpxを使用（タイムアウト10秒推奨）
- データ構造はpydantic BaseModelで定義
- すべての関数に型アノテーションを付ける

## インフラストラクチャ

Terraformによるインフラ管理（`infra/terraform/`）

```bash
cd infra/terraform/environments/dev  # or prod
terraform init
terraform plan
terraform apply
```

環境分離

- `environments/dev/`: 開発環境
- `environments/prod/`: 本番環境
- `modules/`: 再利用可能モジュール

コード品質

```bash
terraform fmt -recursive
terraform validate
```

詳細は `infra/terraform/README.md` を参照。
