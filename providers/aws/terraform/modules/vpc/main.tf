module "vpc" {
  # Use terraform vpc module from registry - https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest
  source = "terraform-aws-modules/vpc/aws"
  version = "~> 2.0"

  name = var.vpc_name
  cidr = var.cidr

  azs = var.azs
  public_subnets = var.public_subnets


  enable_dns_hostnames = var.enable_dns_hostnames

  tags = {
    Environment = var.environment
  }
}
