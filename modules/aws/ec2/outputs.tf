output "public_ip" {
  description = "The name of the key"
  value = aws_instance.this_instance.*.public_ip
}

output "fqdn" {
  description = "The name of the key"
  value = aws_route53_record.dns_record.*.fqdn
}