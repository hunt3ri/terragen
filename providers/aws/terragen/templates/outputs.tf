{% for key, value in outputs.items() %}
output "{{ key }}" {
  description = "{{ value.description }}"
  value = module.{{ module_name }}.{{ key }}
}

{%- endfor %}