# -*- coding: utf-8 -*-
import os
from pathlib import Path

import mkdocs_gen_files
from kiara import Kiara

kiara = Kiara.instance()

modules_file_path = os.path.join("modules_list.md")

BASE_PACKAGE = "kiara_documentation"

operations_base_path = os.path.join("concepts", "operations", "operation_types")
template_path = os.path.join(os.path.dirname(__file__), "operation_type_template.md")
page_content = Path(template_path).read_text()

for op_type in kiara.operation_mgmt.operation_types.keys():

    if op_type == "all":
        continue

    op_type_page_path = os.path.join(operations_base_path, f"{op_type}.md")
    op_type_content = page_content.replace("__OP_TYPE_VALUE__", op_type)
    with mkdocs_gen_files.open(op_type_page_path, "w") as f:
        f.write(op_type_content)
