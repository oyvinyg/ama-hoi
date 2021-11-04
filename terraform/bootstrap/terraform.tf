terraform {
  required_version = "~> 1.0.4"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.24"
    }
  }

  backend "s3" {
    bucket         = "bootstrap-terraform-dev"
    key            = "ama-hoi/terraform.tfstate"
    region         = "eu-west-1"
    encrypt        = true
    dynamodb_table = "bootstrap-terraform-state-lock"
  }
}

provider "aws" {
  region  = "eu-west-1"
  profile = "knowit-playground"
}

provider "template" {}
