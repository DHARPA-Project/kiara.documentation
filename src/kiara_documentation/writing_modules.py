# -*- coding: utf-8 -*-
from kiara import KiaraModule
from pandas import DataFrame


class MyFirstModule(KiaraModule):

    _module_type_name = "filter_table_by_date"

    def create_input_schema(self):
        return {
            "table_input": {"type": "table", "doc": "The table that will be filtered."},
            "date": {
                "type": "date",
                "doc": "The minimum date, earlier dates will be filtered out.",
            },
        }

    def create_output_schema(self):
        return {"table_output": {"type": "table", "doc": "The filtered table."}}

    def process(self, inputs, outputs) -> None:
        pass


class FilterTableByDate2Module(KiaraModule):

    _module_type_name = "filter_table_by_date_2"

    def create_input_schema(self):
        return {
            "table_input": {"type": "table", "doc": "The table that will be filtered."},
            "date": {
                "type": "date",
                "doc": "The minimum date, earlier dates will be filtered out.",
            },
        }

    def create_output_schema(self):
        return {"table_output": {"type": "table", "doc": "The filtered table."}}

    def process(self, inputs, outputs) -> None:

        table_obj = inputs.get_value_data("table_input")
        outputs.set_value("table_output", table_obj)


class FilterTableByDate3Module(KiaraModule):

    _module_type_name = "filter_table_by_date_3"

    def create_input_schema(self):
        return {
            "table_input": {"type": "table", "doc": "The table that will be filtered."},
            "date": {
                "type": "date",
                "doc": "The minimum date, earlier dates will be filtered out.",
            },
        }

    def create_output_schema(self):
        return {"table_output": {"type": "table", "doc": "The filtered table."}}

    def process(self, inputs, outputs):

        table_obj = inputs.get_value_data("table_input")
        date_input = inputs.get_value_data("date")

        print("------")
        print(f"HELLO FROM INSIDE THE MODULE, THIS IS OUR DATE: {date_input}")
        print("------")

        outputs.set_value("table_output", table_obj)


class FilterTableByDate4Module(KiaraModule):

    _module_type_name = "filter_table_by_date_4"

    def create_input_schema(self):
        return {
            "table_input": {"type": "table", "doc": "The table that will be filtered."},
            "date": {
                "type": "date",
                "doc": "The minimum date, earlier dates will be filtered out.",
            },
        }

    def create_output_schema(self):
        return {"table_output": {"type": "table", "doc": "The filtered table."}}

    def process(self, inputs, outputs):

        table_obj = inputs.get_value_data("table_input")
        date_input = inputs.get_value_data("date")

        df: DataFrame = table_obj.to_pandas()

        after_date = df[df["birthday"] >= date_input.date()]

        import pyarrow as pa

        result_table = pa.Table.from_pandas(after_date, preserve_index=False)

        outputs.set_value("table_output", result_table)
