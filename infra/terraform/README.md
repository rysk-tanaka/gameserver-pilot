# Terraform Infrastructure

gameserver-pilot のインフラストラクチャを管理する Terraform 構成。

## ディレクトリ構成

```tree
terraform/
├── environments/
│   ├── dev/      # 開発環境
│   └── prod/     # 本番環境
└── modules/      # 再利用可能モジュール
```

## セットアップ

### 前提条件

- Terraform >= 1.0
- AWS CLI（認証設定済み）

### 初期化

```bash
cd environments/dev  # or prod
cp terraform.tfvars.example terraform.tfvars
# terraform.tfvars を編集

terraform init
terraform plan
terraform apply
```

## リモートステート設定

S3バケットとDynamoDBテーブルを作成後、`backend.tf` のコメントを解除してください。

```bash
# S3バケット作成（例）
aws s3api create-bucket \
  --bucket gameserver-pilot-tfstate \
  --region ap-northeast-1 \
  --create-bucket-configuration LocationConstraint=ap-northeast-1

# DynamoDBテーブル作成（例）
aws dynamodb create-table \
  --table-name gameserver-pilot-tfstate-lock \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region ap-northeast-1
```

## 環境の違い

| 項目 | dev | prod |
|------|-----|------|
| tfstate key | `dev/terraform.tfstate` | `prod/terraform.tfstate` |
| default_tags.Environment | `dev` | `prod` |

## TODO

- [ ] S3バケット・DynamoDBテーブル作成（リモートステート用）
- [ ] `backend.tf` のコメント解除
- [ ] `modules/ec2-gameserver` モジュール作成
  - EC2インスタンス
  - セキュリティグループ
  - IAMロール（必要に応じて）
- [ ] `modules/networking` モジュール作成（必要に応じて）
  - VPC
  - サブネット
  - インターネットゲートウェイ
