terraform {
  required_version = "~> 1.0.4"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.24"
    }

    template = {
      source  = "hashicorp/template"
      version = "~> 2.2"
    }
  }

  backend "s3" {
    bucket         = "ama-hoi-terraform-prod"
    key            = "ama-hoi/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "ama-hoi-terraform-lock-table-prod"
  }
}

provider "aws" {
  region  = "eu-west-1"
  profile = "knowit-playground"
}

provider "template" {}
