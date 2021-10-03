module "{{ module_name }}" {
  # Module documentation at link - {{ module_url }}
  source = "{{ module_source }}"
  version = "{{ module_version }}"

{% for key, value in module_config.items() %}
  {{ to_toml(key, value) }}
{%- endfor %}

  tags = {
    {% for key, value in tags.items() -%}
    {{ to_toml(key, value) }}
    {%- endfor %}
  }
}