# Beszel セットアップガイド

## 概要

このガイドでは、Beszelリソース監視システムのセットアップ手順を説明します。
設計の詳細については [beszel-monitoring.md](./beszel-monitoring.md) を参照してください。

## 前提条件

- Railwayアカウント
- Discordサーバーの管理権限
- AWS EC2インスタンス（監視対象）

## 1. Beszel Hub のデプロイ（Railway）

### 1.1 テンプレートからデプロイ

以下のURLからワンクリックでデプロイできます。

<https://railway.com/deploy/nJKarX>

### 1.2 ボリューム設定

デプロイ後、永続化のためボリュームを追加します。

1. Railwayダッシュボードでプロジェクトを開く
2. Beszel Hubサービスを選択
3. 「Volumes」タブで新規ボリュームを追加
4. マウントパス: `/beszel_data`

### 1.3 初期設定

1. デプロイされたHubのURLにアクセス
2. 管理者アカウントを作成
3. メールアドレスとパスワードをメモ（Discord Bot用）

## 2. Discord Bot 環境変数

Railwayの gameserver-pilot サービスに以下の環境変数を追加します。

| 変数名 | 説明 | 例 |
|--------|------|------|
| `BESZEL_HUB_URL` | Beszel HubのURL | `https://beszel-xxx.railway.app` |
| `BESZEL_EMAIL` | Hub管理者メール | `admin@example.com` |
| `BESZEL_PASSWORD` | Hub管理者パスワード | `secure-password` |
| `BESZEL_REPORT_CHANNEL_ID` | レポート送信先チャンネルID | `123456789012345678` |

### チャンネルIDの取得方法

1. Discordの設定で「開発者モード」を有効化
2. 対象チャンネルを右クリック →「IDをコピー」

## 3. Beszel Agent のインストール（EC2）

### 3.1 Hub でシステム追加

1. Beszel Hub UIにログイン
2. 「Add System」をクリック
3. 「WebSocket」モードを選択
4. 表示されるトークンとSSH公開鍵をコピー

### 3.2 EC2 にエージェントをインストール

EC2インスタンスにSSH接続し、以下を実行します。

```bash
curl -sL https://get.beszel.dev/agent | bash -s -- \
  --hub-url "https://your-beszel-hub.railway.app" \
  --token "your-registration-token" \
  --key "ssh-ed25519 AAAAC3..." \
  --auto-update
```

または、Docker Compose を使用する場合。

```yaml
services:
  beszel-agent:
    image: henrygd/beszel-agent:latest
    container_name: beszel-agent
    restart: unless-stopped
    network_mode: host
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    environment:
      HUB_URL: "https://your-beszel-hub.railway.app"
      TOKEN: "${BESZEL_TOKEN}"
      KEY: "${BESZEL_KEY}"
```

### 3.3 systemd での自動起動確認

バイナリインストールの場合、自動的にsystemdサービスが設定されます。

```bash
# ステータス確認
sudo systemctl status beszel-agent

# ログ確認
sudo journalctl -u beszel-agent -f
```

## 4. アラート設定

### 4.1 Discord Webhook の作成

1. Discordサーバー設定 →「連携サービス」→「ウェブフック」
2. 新しいウェブフックを作成
3. 対象チャンネルを選択
4. WebhookのURLをコピー

形式: `https://discord.com/api/webhooks/{webhook_id}/{token}`

### 4.2 Beszel Hub でアラート設定

1. Hub UIで「Settings」→「Notifications」
2. 「Add Notification」をクリック
3. Shoutrrr形式でURLを入力

```text
discord://{token}@{webhook_id}
```

例: URLが `https://discord.com/api/webhooks/123/abc` の場合
→ `discord://abc@123`

### 4.3 推奨アラート閾値

各システムで以下のアラートを設定します。

| メトリクス | 閾値 | 説明 |
|-----------|------|------|
| CPU | > 80% | 高負荷検知 |
| Memory | > 90% | メモリ逼迫 |
| Disk | > 85% | ストレージ不足 |
| Status | offline | サーバーダウン |

設定手順。

1. Hub UIでシステムを選択
2. 「Alerts」タブを開く
3. 各メトリクスの閾値を設定

## 5. トラブルシューティング

### Agent が Hub に接続できない

1. EC2のSecurity Groupでアウトバウンド443が許可されているか確認

   ```bash
   # EC2から接続テスト
   curl -I https://your-beszel-hub.railway.app
   ```

2. トークンとキーが正しいか確認

### メトリクスが更新されない

```bash
# Agent プロセスの確認
sudo systemctl status beszel-agent

# 再起動
sudo systemctl restart beszel-agent
```

### Discord に通知が来ない

1. Shoutrrr URLの形式を確認（`discord://token@webhook_id`）
2. Hub UIで「Test」ボタンを押してテスト通知を送信

### Bot からデータ取得できない

認証トークンの期限切れの可能性があります。
Botを再起動してトークンをリフレッシュしてください。

## 6. バックアップ

### S3 連携（推奨）

1. Hub管理画面で `/_/#/settings/backups` にアクセス
2. S3バケット情報を設定
3. 自動バックアップスケジュールを設定

### 手動バックアップ

Railway CLI を使用してボリュームをエクスポートできます。

```bash
railway volume export --mount /beszel_data
```
