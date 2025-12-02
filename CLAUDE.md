# CLAUDE.md - gameserver-pilot

リアルタイムマルチプレイヤーゲーム向けのスケーラブルなゲームサーバーフレームワーク

## 技術スタック

- **言語**: Python 3.14+
- **パッケージマネージャー**: uv
- **データバリデーション**: pydantic, pydantic-settings
- **HTTP通信**: httpx
- **設定ファイル**: PyYAML
- **テスト**: pytest, pytest-cov, pytest-asyncio
- **コード品質**: ruff (フォーマット/リント), mypy (型チェック)

## プロジェクト構成

```
gameserver-pilot/
├── gameserver_pilot/           # メインパッケージ
│   ├── __init__.py             # パッケージ初期化、エントリーポイント
│   ├── server.py               # GameServerクラス
│   ├── config.py               # ServerConfig (pydantic-settings)
│   ├── models/                 # データモデル
│   │   ├── player.py           # Playerモデル
│   │   └── game_state.py       # GameStateモデル
│   ├── networking/             # ネットワーク処理
│   │   └── connection.py       # Connectionクラス
│   ├── game/                   # ゲームロジック
│   │   └── loop.py             # GameLoopクラス
│   └── utils/                  # ユーティリティ
│       └── id_generator.py     # ID生成関数
├── tests/                      # テストスイート
│   ├── test_server.py          # サーバーテスト
│   ├── models/                 # モデルテスト
│   ├── networking/             # ネットワークテスト
│   └── game/                   # ゲームロジックテスト
├── docs/                       # ドキュメント
├── config/                     # 設定ファイル
└── cache/                      # キャッシュディレクトリ
```

## 開発コマンド

```bash
# 依存関係のインストール
uv sync --group dev

# サーバー起動
uv run gameserver-pilot

# テスト実行
uv run pytest

# カバレッジ付きテスト
uv run pytest --cov=gameserver_pilot --cov-report=html

# フォーマット
uv run ruff format .

# リント
uv run ruff check .

# リント自動修正
uv run ruff check --fix .

# 型チェック
uv run mypy gameserver_pilot
```

## コード規約

### ruff設定 (pyproject.toml)

- 行長: 100文字
- 有効ルール: E, W, F (エラー/警告), UP (pyupgrade), B (bugbear), I (isort), PLR (pylint refactor)
- 複雑度上限: 10
- 関数引数上限: 8
- 分岐上限: 15
- 文数上限: 50

### mypy設定

- pydanticプラグイン有効
- strictモードを目指す

### テスト規約

- テストファイルは `test_*.py` 形式
- テスト関数は `test_*` 形式
- モデルテストは `tests/models/` に配置
- ネットワークテストは `tests/networking/` に配置
- ゲームロジックテストは `tests/game/` に配置

## 主要クラス

### GameServer (`gameserver_pilot/server.py`)

メインサーバークラス。接続管理とゲーム状態を統括。

```python
from gameserver_pilot import GameServer
from gameserver_pilot.config import ServerConfig

config = ServerConfig(port=9000, max_players=50)
server = GameServer(config=config)
server.run()
```

### ServerConfig (`gameserver_pilot/config.py`)

サーバー設定。環境変数から読み込み可能（プレフィックス: `GAMESERVER_`）

- `host`: バインドアドレス (default: "0.0.0.0")
- `port`: ポート番号 (default: 8080)
- `tick_rate`: Tick/秒 (default: 60)
- `max_players`: 最大プレイヤー数 (default: 100)
- `log_level`: ログレベル (default: "info")

### Player (`gameserver_pilot/models/player.py`)

プレイヤーモデル。pydantic BaseModel。

- `id`: ユニークID (必須)
- `name`: 表示名 (必須)
- `x`, `y`: 座標 (default: 0.0)
- `score`: スコア (default: 0)
- `connected`: 接続状態 (default: True)

### GameState (`gameserver_pilot/models/game_state.py`)

ゲーム状態モデル。プレイヤー管理メソッドを持つ。

- `add_player(player)`: プレイヤー追加
- `remove_player(player_id)`: プレイヤー削除
- `get_player(player_id)`: プレイヤー取得

### GameLoop (`gameserver_pilot/game/loop.py`)

固定Tickレートのゲームループ。コールバック登録可能。

## 環境変数

```bash
GAMESERVER_HOST=0.0.0.0
GAMESERVER_PORT=8080
GAMESERVER_TICK_RATE=60
GAMESERVER_MAX_PLAYERS=100
GAMESERVER_LOG_LEVEL=info
```

## AI向けガイドライン

### 実装時の注意点

1. **pydanticモデルを使用**: データ構造はpydantic BaseModelで定義
2. **型アノテーション必須**: すべての関数に型アノテーションを付ける
3. **テスト必須**: 新機能には対応するテストを追加
4. **httpxを使用**: HTTP通信はhttpxを使用（タイムアウト10秒を推奨）

### コードスタイル

- インポートはisortでソート（ruffが自動処理）
- docstringは簡潔に（複雑なロジックのみ詳細に）
- 1関数1責務を心がける

### 避けるべきこと

- グローバル状態の使用
- 同期的なブロッキングI/O（非同期を優先）
- クライアント入力の無検証での使用
- 過度な抽象化

---

*Last updated: 2025-12-02*
