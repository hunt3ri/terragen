data "terraform_remote_state" "vpc" {
  # Get global VPC vars
  backend = "s3"

  config = {
    bucket                  = var.bucket
    key                     = "common/vpc/{% vpc_name %}/terraform.tfstate"
    region                  = var.region
    profile                 = var.profile
  }
}
