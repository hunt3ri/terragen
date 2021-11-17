#################
# Security Group
#################

variable "sg_name" {
  description = "Name of security group"
}

variable "sg_description" {
  description = "Description of security group"
}

variable "ingress_cidr_blocks" {
  description = "List of IPv4 CIDR ranges to use on all ingress rules"
}

variable "ingress_rules" {
  description = "List of ingress rules to create by name"
}

#################
# EC2
#################
variable "instance_count" {
  description = "Number of instances to create"
  default = 1
}

variable "instance_name" {
  description = "Name to be used on all resources as prefix"
}

variable "instance_type" {
  description = "Type of EC2 instance to create"
  default = "t3a.small"
}

variable "associate_public_ip_address" {
  description = "If true, the EC2 instance will have associated public IP address"
  default = False
}

variable "aws_account" {
  description = "The ID of the AWS account we're operating in"
}
