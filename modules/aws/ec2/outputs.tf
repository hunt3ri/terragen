output "fqdn" {
  description = "The name of the key"
  value = aws_route53_record.sandbox_dns_record.*.fqdn
}