
module "sandbox_sg" {
  # SG registry module https://registry.terraform.io/modules/terraform-aws-modules/security-group/aws/latest
  source               = "terraform-aws-modules/security-group/aws"
  version              = "~> 4.0"

  name                 = var.sg_name
  description          = var.sg_description
  vpc_id               = data.terraform_remote_state.vpc.outputs.vpc_id

  ingress_cidr_blocks  = var.ingress_cidr_blocks
  ingress_rules        = var.ingress_rules

  egress_rules         = ["all-all"]
}

resource "aws_instance" "sandbox" {
  # Create EC2 Sandbox Instance(s) using base ubuntu AMI
  count                       = var.instance_count
  ami                         = data.aws_ami.hunter_labs_sandbox.id
  instance_type               = var.instance_type

  subnet_id                   = data.terraform_remote_state.vpc.outputs.public_subnet_ids[count.index]
  associate_public_ip_address = var.associate_public_ip_address
  vpc_security_group_ids      = [module.sandbox_sg.security_group_id]

  key_name                    = data.terraform_remote_state.key_pair.outputs.key_name

  tags = {
    Name = "${var.instance_name}-${count.index + 1}"
  }
}
