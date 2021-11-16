variable "key_name" {
  description = "The name for the key pair"
}

variable "public_key" {
  description = "The CIDR block for the VPC."
}

variable "owner" {
  description = "Owner of the key pair resource"
  default = "Hunter-Labs"
}
