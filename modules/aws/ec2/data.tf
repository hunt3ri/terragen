data "terraform_remote_state" "vpc" {
  # Get global VPC vars
  backend = "s3"

  config = {
    bucket                  = var.bucket
    key                     = "{{ vpc_statefile }}"
    region                  = var.region
    profile                 = var.profile
  }
}
