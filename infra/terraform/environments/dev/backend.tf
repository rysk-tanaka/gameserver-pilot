# Uncomment after creating the S3 bucket and DynamoDB table for state management
#
# terraform {
#   backend "s3" {
#     bucket         = "gameserver-pilot-tfstate"
#     key            = "dev/terraform.tfstate"
#     region         = "ap-northeast-1"
#     encrypt        = true
#     dynamodb_table = "gameserver-pilot-tfstate-lock"
#   }
# }
