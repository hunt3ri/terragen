terraform {
  required_providers {
    aws = {
      version = ">= 3.0"
      source  = "hashicorp/aws"
    }
  }
  backend "s3" {
    key     = "{{ s3_backend_key }}/terraform.tfstate"
  }
}

provider "aws" {
  profile                 = var.profile  # Read from environment var TF_VAR_profile
  region                  = var.region   # Read from environment var TF_VAR_region
}
