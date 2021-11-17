resource "aws_key_pair" "keypair" {
  # Generate Key to allow ssh access
  key_name   = var.key_name
  public_key = var.public_key
  tags = {
    owner = var.owner
  }
}
