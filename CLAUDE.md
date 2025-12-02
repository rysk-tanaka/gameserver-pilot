# CLAUDE.md - gameserver-pilot

ゲームサーバーをDiscordから操作し、プレイヤー不在時に自動停止するシステム

## 技術スタック

- **言語**: Python 3.14+
- **パッケージマネージャー**: uv
- **Discord Bot**: discord.py
- **AWS操作**: boto3
- **HTTP通信**: httpx
- **データバリデーション**: pydantic, pydantic-settings
- **テスト**: pytest, pytest-cov, pytest-asyncio
- **コード品質**: ruff (フォーマット/リント), mypy (型チェック)

## プロジェクト構成

```
gameserver-pilot/
├── gameserver_pilot/
│   ├── __init__.py
│   ├── bot.py                 # Discord Bot メイン
│   ├── config.py              # 設定 (pydantic-settings)
│   ├── cloud/                 # クラウドプロバイダー
│   │   ├── __init__.py
│   │   ├── base.py           # 抽象クラス CloudProvider
│   │   ├── ec2.py            # AWS EC2実装
│   │   └── mock.py           # 開発用モック
│   └── monitors/              # プレイヤー監視
│       ├── __init__.py
│       ├── base.py           # 抽象クラス PlayerMonitor
│       ├── tshock.py         # TShock REST API監視
│       └── logfile.py        # ログファイル監視
├── tests/
│   ├── test_bot.py
│   ├── cloud/
│   │   └── test_ec2.py
│   └── monitors/
│       ├── test_tshock.py
│       └── test_logfile.py
├── pyproject.toml
└── README.md
```

## 開発コマンド

```bash
# 依存関係のインストール
uv sync --group dev

# Bot起動（開発モード）
ENV=development uv run python -m gameserver_pilot.bot

# Bot起動（本番モード）
ENV=production uv run python -m gameserver_pilot.bot

# テスト実行
uv run pytest

# カバレッジ付きテスト
uv run pytest --cov=gameserver_pilot --cov-report=html

# フォーマット
uv run ruff format .

# リント
uv run ruff check .

# 型チェック
uv run mypy gameserver_pilot
```

## コード規約

### ruff設定 (pyproject.toml)

- 行長: 100文字
- 有効ルール: E, W, F, UP, B, I, PLR
- 複雑度上限: 10
- 関数引数上限: 8

### テスト規約

- テストファイルは `test_*.py` 形式
- cloud テストは `tests/cloud/` に配置
- monitors テストは `tests/monitors/` に配置
- モックを使用してAWS APIをテスト

## 主要クラス

### CloudProvider (`gameserver_pilot/cloud/base.py`)

クラウドプロバイダーの抽象基底クラス。

```python
from abc import ABC, abstractmethod

class CloudProvider(ABC):
    @abstractmethod
    async def start_server(self, server_id: str) -> bool: ...

    @abstractmethod
    async def stop_server(self, server_id: str) -> bool: ...

    @abstractmethod
    async def get_server_status(self, server_id: str) -> str: ...
```

### EC2Provider (`gameserver_pilot/cloud/ec2.py`)

AWS EC2の実装。boto3を使用。

### MockProvider (`gameserver_pilot/cloud/mock.py`)

開発・テスト用のモック実装。

### PlayerMonitor (`gameserver_pilot/monitors/base.py`)

プレイヤー監視の抽象基底クラス。

```python
from abc import ABC, abstractmethod

class PlayerMonitor(ABC):
    @abstractmethod
    async def get_player_count(self) -> int: ...
```

### TShockMonitor (`gameserver_pilot/monitors/tshock.py`)

TShock REST APIを使用したプレイヤー数取得。

### LogFileMonitor (`gameserver_pilot/monitors/logfile.py`)

ログファイルを監視してプレイヤー数を取得。

## 環境変数

```bash
# Discord
DISCORD_TOKEN="your-bot-token"

# AWS
AWS_ACCESS_KEY_ID="your-access-key"
AWS_SECRET_ACCESS_KEY="your-secret-key"
AWS_DEFAULT_REGION="ap-northeast-1"

# 動作モード
ENV="development"  # or "production"

# 自動停止設定
AUTO_STOP_MINUTES=60  # プレイヤー0人での自動停止までの時間
```

## Discordスラッシュコマンド

| コマンド | 説明 |
|---------|------|
| `/start <server>` | サーバーを起動 |
| `/stop <server>` | サーバーを停止 |
| `/status <server>` | サーバー状態を確認 |

## 対応ゲーム

| ゲーム | Monitor クラス | 取得方式 |
|--------|---------------|---------|
| Terraria (TShock) | TShockMonitor | REST API |
| Terraria (Vanilla) | LogFileMonitor | ログファイル監視 |
| Core Keeper | LogFileMonitor | ログファイル監視 |

## AI向けガイドライン

### 実装時の注意点

1. **抽象クラスを継承**: CloudProviderとPlayerMonitorを継承して実装
2. **非同期を使用**: すべてのI/O操作はasync/awaitを使用
3. **pydanticモデルを使用**: データ構造はpydantic BaseModelで定義
4. **型アノテーション必須**: すべての関数に型アノテーションを付ける
5. **テスト必須**: 新機能には対応するテストを追加
6. **httpxを使用**: HTTP通信はhttpxを使用（タイムアウト10秒を推奨）

### 新しいゲームの追加方法

1. `monitors/` に新しいMonitorクラスを作成
2. `PlayerMonitor` を継承し `get_player_count()` を実装
3. 対応するテストを `tests/monitors/` に追加
4. README.mdの対応ゲーム表を更新

### 新しいクラウドプロバイダーの追加方法

1. `cloud/` に新しいProviderクラスを作成
2. `CloudProvider` を継承し各メソッドを実装
3. 対応するテストを `tests/cloud/` に追加

### 避けるべきこと

- グローバル状態の使用
- 同期的なブロッキングI/O
- AWS認証情報のハードコード
- 入力の無検証での使用

---

*Last updated: 2025-12-02*
