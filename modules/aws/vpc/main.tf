module "vpc" {
  # Module documentation at link - https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest
  source = "terraform-aws-modules/vpc/aws"
  version = "~> 3.0"

  name = var.vpc_name
  cidr = var.cidr
  azs = var.azs
  public_subnets = var.public_subnets
  enable_dns_hostnames = var.enable_dns_hostnames

  tags = {
    environment = var.environment
  }
}
