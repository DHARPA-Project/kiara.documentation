---
title: __OP_TYPE_VALUE__
---
{% set operation_type="__OP_TYPE_VALUE__" -%}
{% set operation_info = get_kiara_context().operations.operation_types[operation_type] %}
{{ operation_info.info.documentation.full_doc }}

## Available operations

{% for operation_id, operation in operation_info.operation_configs.items() %}
- ``{{ operation_id }}``: {{ operation["doc"].description }}
{% endfor %}
