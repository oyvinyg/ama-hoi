data "aws_caller_identity" "this" {}
data "aws_region" "current" {}

locals {
  name   = "ama-hoi"
  account_id = data.aws_caller_identity.this.account_id
  region     = data.aws_region.current.name
  tags = {
    Owner       = "ama-hoi"
    Environment = "dev"
  }
}