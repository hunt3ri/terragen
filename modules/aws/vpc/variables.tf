###########
# VPC
###########

variable "vpc_name" {
  description = "Name to be used on all the resources as identifier"
}

variable "cidr" {
  description = "The CIDR block for the VPC."
}

variable "azs" {
  description = "A list of availability zones names or ids in the region"
}

variable "public_subnets" {
  description = "A list of public subnet cidr ranges inside the VPC, should match azs"
}

variable "enable_dns_hostnames" {
  description = "Set to true to enable DNS hostnames in the VPC, will generate public dns name for EC2 instance"
}
