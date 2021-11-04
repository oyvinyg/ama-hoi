locals {
  bucket_name = "ama-hoi-terraform-${var.env}"
  lock_table_name = "ama-hoi-terraform-lock-table-${var.env}"
}

/* Bucket for storing logs */
resource "aws_s3_bucket" "game_server_logs_bucket" {
  bucket = "ama-hoi-logs-${var.env}"
  acl    = "log-delivery-write"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    Name        = "ama-hoi logs bucket"
    Environment = var.env
  }
}


/* Bucket for storing config, e.g. Terraform state */
resource "aws_s3_bucket" "game_server_config_bucket" {
  bucket = local.bucket_name
  acl    = "private"

  versioning {
    enabled = true
  }

  logging {
    target_bucket = aws_s3_bucket.game_server_logs_bucket.id
    target_prefix = "logs/s3/${local.bucket_name}/"
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    Name        = "ama-hoi configuration bucket"
    Environment = var.env
  }
}

/* DynamoDB lock table for Terraform state */
resource "aws_dynamodb_table" "terraform_state_lock_table" {
  name           = local.lock_table_name
  hash_key       = "LockID"
  read_capacity  = 1
  write_capacity = 1

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name = "ama-hoi terraform state lock table"
  }

  point_in_time_recovery {
    enabled = true
  }
}
