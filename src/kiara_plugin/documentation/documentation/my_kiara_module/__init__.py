# -*- coding: utf-8 -*-

from kiara.models.values.value import ValueMap
from kiara.modules import (
    KiaraModule,
    KiaraModuleConfig,
    ModuleCharacteristics,
    ValueSetSchema,
)
from pydantic import Field


class ExampleModuleConfig(KiaraModuleConfig):

    separator: str = Field(
        description="The seperator between the two strings.", default=" - "
    )


class ExampleModule(KiaraModule):
    """A very simple example module; concatenate two strings.

    The purpose of this modules is to show the main elements of a [`KiaraModule`][kiara.modules.KiaraModule]:

    - ***the (optional) configuration class***: must inherit from [`KiaraModuleConfig`][kiara.modules.KiaraModuleConfig], and the config class must be set as the `_config_cls` attribute
         on the `KiaraModule` class. Configuration values can be retrieved via the [`self.get_config_value(key)`][kiara.modules.KiaraModule.get_config_value] method
    - ***the inputs description***: must return a dictionary, containing the input name(s) as keys, and another dictionary containing type_name information
         and documentation about the input data as value
    - ***the outputs description***: must return a dictionary, containing the output name(s) as keys, and another dictionary containing type_name information
         and documentation about the output data as value
    - ***the ``process`` method***: this is where the actual work gets done. Input data can be accessed via ``inputs.get_value_data(key)``, results
         can be set with the ``outputs.set_value(key, value)`` method

    Example:

        This example module can be tested on the commandline with the ``kiara run`` command:

        ```
        kiara run core_types.example text_1="xxx" text_2="yyy"
        ```
    """

    _config_cls = ExampleModuleConfig
    _module_type_name = "my_kiara_module.example"

    def create_inputs_schema(
        self,
    ) -> ValueSetSchema:

        inputs = {
            "text_1": {"type": "string", "doc": "The first text."},
            "text_2": {"type": "string", "doc": "The second text."},
        }

        return inputs

    def create_outputs_schema(
        self,
    ) -> ValueSetSchema:

        outputs = {
            "text": {
                "type": "string",
                "doc": "The concatenated text.",
            }
        }
        return outputs

    def process(self, inputs: ValueMap, outputs: ValueMap) -> None:

        separator = self.get_config_value("separator")

        text_1 = inputs.get_value_data("text_1")
        text_2 = inputs.get_value_data("text_2")

        result = text_1 + separator + text_2
        outputs.set_value("text", result)


class TutorialModule(KiaraModule):
    _module_type_name = "kiara_plugin.my_kiara_module.my_kiara_module.tutorial_module"

    def create_inputs_schema(self):
        return {"table": {"type": "table"}}

    def create_outputs_schema(self):
        return {"table": {"type": "table"}}

    def process(self, inputs, outputs) -> None:
        pass


class TutorialModule1(KiaraModule):
    """Filter a table."""

    _module_type_name = "filter.table"

    def create_inputs_schema(self):
        return {"table_input": {"type": "table"}}

    def create_outputs_schema(self):
        return {"table_output": {"type": "table"}}

    def process(self, inputs, outputs) -> None:
        pass


class TutorialModule2(KiaraModule):
    """Filter a table."""

    _module_type_name = "filter.table_2"

    def _retrieve_module_characteristics(self) -> ModuleCharacteristics:

        return ModuleCharacteristics(is_internal=True)

    def create_inputs_schema(self):
        return {"table_input": {"type": "table", "doc": "The table to filter."}}

    def create_outputs_schema(self):
        return {"table_output": {"type": "table", "doc": "The filtered table."}}

    def process(self, inputs, outputs) -> None:

        table_obj = inputs.get_value_obj("table_input")

        print(f"Filter module, table input value: {table_obj}")
        print(f"Table data instance: {table_obj.data}")

        outputs.set_value("table_output", table_obj)


class TutorialModule3(KiaraModule):
    """Filter a table."""

    _module_type_name = "filter.table_3"

    def _retrieve_module_characteristics(self) -> ModuleCharacteristics:

        return ModuleCharacteristics(is_internal=True)

    def create_inputs_schema(self):
        return {"table_input": {"type": "table", "doc": "The table to filter."}}

    def create_outputs_schema(self):
        return {"table_output": {"type": "table", "doc": "The filtered table."}}

    def process(self, inputs, outputs) -> None:

        table_obj = inputs.get_value_obj("table_input")

        print(f"Filter module, table input value: {table_obj}")
        print(f"Table data instance: {table_obj.data}")

        pandas_df = table_obj.data.to_pandas()
        print(f"Column names: {pandas_df.columns}")

        outputs.set_value("table_output", table_obj)


class TutorialModule4(KiaraModule):
    """Filter a table."""

    _module_type_name = "filter.table_4"

    def _retrieve_module_characteristics(self) -> ModuleCharacteristics:

        return ModuleCharacteristics(is_internal=True)

    def create_inputs_schema(self):
        return {"table_input": {"type": "table", "doc": "The table to filter."}}

    def create_outputs_schema(self):
        return {"table_output": {"type": "table", "doc": "The filtered table."}}

    def process(self, inputs, outputs) -> None:

        from kiara.exceptions import KiaraProcessingException

        table_obj = inputs.get_value_obj("table_input")
        pandas_df = table_obj.data.to_pandas()

        column_names = pandas_df.columns
        if "City" not in column_names:
            raise KiaraProcessingException(
                "Invalid table, does not contain a column named 'City'."
            )

        berlin_df = pandas_df.loc[pandas_df["City"] == "Berlin"]
        outputs.set_value("table_output", berlin_df)


class TutorialModule5(KiaraModule):
    """Filter a table."""

    _module_type_name = "filter.table_5"

    def _retrieve_module_characteristics(self) -> ModuleCharacteristics:

        return ModuleCharacteristics(is_internal=True)

    def create_inputs_schema(self):
        return {
            "table_input": {"type": "table", "doc": "The table to filter."},
            "column_name": {
                "type": "string",
                "doc": "The column containing the element to use as filter.",
                "default": "City",
            },
            "filter_string": {"type": "string", "doc": "The string to use as filter."},
        }

    def create_outputs_schema(self):
        return {"table_output": {"type": "table", "doc": "The filtered table."}}

    def process(self, inputs, outputs) -> None:

        from kiara.exceptions import KiaraProcessingException

        table_obj = inputs.get_value_obj("table_input")
        column_name = inputs.get_value_data("column_name")
        filter_string = inputs.get_value_data("filter_string")

        pandas_df = table_obj.data.to_pandas()

        column_names = pandas_df.columns
        if column_name not in column_names:
            raise KiaraProcessingException(
                f"Invalid table, does not contain a column named '{column_name}'. Available column names: {', '.join(column_names)}."
            )

        berlin_df = pandas_df.loc[pandas_df[column_name] == filter_string]
        outputs.set_value("table_output", berlin_df)
