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