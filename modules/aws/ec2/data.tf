data "terraform_remote_state" "vpc" {
  # Get global VPC vars
  backend = "s3"

  config = {
    bucket                  = "{{ bucket }}"
    key                     = "{{ lookups['vpc_statefile'] }}"
    region                  = "{{ region }}"
    profile                 = "{{ profile }}"
  }
}
