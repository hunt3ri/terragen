resource "{{ resource_type }}" "keypair" {
  # Generate Key to allow ssh access
{% for key, value in module_config.items() %}
  {{ key }} = {{ value }}
{%- endfor %}
}