# gameserver-pilot

リアルタイムマルチプレイヤーゲーム向けのスケーラブルなゲームサーバーフレームワーク

## 概要

gameserver-pilotは、リアルタイムマルチプレイヤーゲームのためのサーバーサイドフレームワークです。低レイテンシ通信、状態同期、マッチメイキングなどの機能を提供します。

## 特徴

- **高性能**: 非同期I/Oによる効率的な接続処理
- **スケーラブル**: 水平スケーリングに対応した設計
- **柔軟性**: プラグイン可能なアーキテクチャ
- **型安全**: Pydanticによるデータバリデーション

## 必要条件

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) パッケージマネージャー

## インストール

```bash
# リポジトリのクローン
git clone https://github.com/rysk-tanaka/gameserver-pilot.git
cd gameserver-pilot

# 依存関係のインストール
uv sync
```

## 開発環境のセットアップ

```bash
# 開発用依存関係を含めてインストール
uv sync --group dev

# pre-commitフックの設定
uv run pre-commit install
```

## 使用方法

```bash
# サーバーの起動
uv run gameserver-pilot

# または
uv run python -m gameserver_pilot
```

## テスト

```bash
# テストの実行
uv run pytest

# カバレッジレポート付きで実行
uv run pytest --cov=gameserver_pilot --cov-report=html
```

## コード品質

```bash
# フォーマット
uv run ruff format .

# リント
uv run ruff check .

# 型チェック
uv run mypy gameserver_pilot
```

## プロジェクト構成

```
gameserver-pilot/
├── gameserver_pilot/       # メインパッケージ
│   ├── models/             # データモデル
│   ├── networking/         # ネットワーク処理
│   ├── game/               # ゲームロジック
│   └── utils/              # ユーティリティ
├── tests/                  # テストスイート
├── docs/                   # ドキュメント
└── config/                 # 設定ファイル
```

## ライセンス

MIT License

## 貢献

1. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
2. 変更をコミット (`git commit -m 'feat: Add amazing feature'`)
3. ブランチをプッシュ (`git push origin feature/amazing-feature`)
4. プルリクエストを作成
