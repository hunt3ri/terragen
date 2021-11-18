output "public_ip" {
  description = "Public IP address of the EC2 instance"
  value = aws_instance.this_instance.*.public_ip
}

output "fqdn" {
  description = "DNS Address of the EC2 instance"
  value = aws_route53_record.dns_record.*.fqdn
}