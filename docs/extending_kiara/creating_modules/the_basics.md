---
title: The basics
description: How to create your own kiara module -- the basics.
tags:
- tutorial
---

# Writing your own *kiara* module - the basics

## Preparation

### Check out the '*kiara* getting started guide'

If you haven't already, it would make sense for you to go through the [*kiara* getting started guide](../../../usage/getting_started/). This will give you a good overview of the relevant *kiara* features, and how the module(s) you are going to write fits in.


### Setting up development environment

To get going, we need a Python virtual environment in which to develop. We'll be using conda for that here, but this will work for normal virtual environments as well. As a first step, install [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) (if you haven't already). Then:

```
conda create -n my_kiara_module python=3.9
conda activate my_kiara_module
conda install -c conda-forge mamba   # this is optional, but makes everything install related much faster, if you don't use it, replace 'mamba' with 'conda' below
mamba install -c conda-forge -c dharpa kiara kiara_plugin.core_types kiara_plugin.tabular
```

!!! note
    For Linux, if you experience errors, you might or  might not have to also execute: `mamba update -c conda-forge libstdcxx-ng`.

After this, the `kiara` command-line application should be available to you, you can test whether that works, for example via `kiara operation list`.

### Creating a *kiara* plugin project

For this tutorial, we'll use a [project template](https://github.com/DHARPA-Project/kiara_plugin.develop/tree/main/kiara_plugin.%7B%7B%20cookiecutter.project_slug%20%7D%7D) to create a bare-bones kiara plugin project, which we will augment with our own module(s).

First we need to install the `cruft` conda package, which we will use to create our project stub:

```
mamba install -c conda-forge cruft
```

Now, we run `cruft` against our template git repo, feel free to change any of the answers to the questions you'll be asked:

```
cruft create https://github.com/DHARPA-Project/kiara_plugin.develop.git

full_name []: Markus Binsteiner
email []: markus@frkl.io
project_name [my-kiara-plugin]: my-kiara-module
project_slug [my_kiara_module]: my_kiara_module
project_short_description [my-kiara-module]: A kiara plugin project for learning to create kiara modules.
github_user [DHARPA-Project]:
anaconda_user [dharpa]:
```

This should have created a new folder, named `kiara_plugin.my_kiara_module`. Next, we initialize and install the new plugin Python project into our conda environment:

```
cd kiara_plugin.my_kiara_module
git init
git checkout -b develop
pip install -e .
```

!!! note
    TODO: explain what happened here?

Once this is done, you should see a new operation called `my_kiara_module.example`:

{{ cli("kiara", "operation", "list", "example", max_height=200, extra_env={"CONSOLE_WIDTH": "140", "KIARA_CONTEXT": "_my_kiara_module"}) }}

!!! note
    The `example` string token at the end of the above command filters the output to operations that match the token.

This module comes as example code with the project template, and is located in the `src/kiara_plugin/my_kiara_module/my_kiara_module.py` Python file. It only serves as an example and blueprint for your own modules, and you can delete the module class within the file if you wish.

### Pre-loading a table dataset

In our tutorial we'll create a module to filter a table. In order to do this we'll need to pre-seed our *kiara* data store with a tabular dataset. Here is the command to run (with the project root as our working directory):

{{ cli("kiara", "run", "--save", "table=journal_nodes_table", "import.table.from.csv_file", "path=examples/data/journals/JournalNodes1902.csv", max_height=200, extra_env={"CONSOLE_WIDTH": "240", "KIARA_CONTEXT": "_my_kiara_module"}) }}

This should have created an item with alias `journal_nodes_table` in the *kiara* data store, which you can confirm with `kiara data list`.

## Writing the *kiara* module

Ok, let's get started and create a *kiara* module that filters a table, using different filter criteria.

### Module skeleton

In most cases you'd delete the example module mentioned above, and create your module in the Python file where the example module was. For the purpose of this tutorial, we can just leave the example module in place, because it can serve as a quick reference for our own module. Use the editor of your choice, and paste the following text below the existing code into `src/kiara_plugin/my_kiara_module/my_kiara_module.py`:

```python
from kiara import KiaraModule

class TutorialModule(KiaraModule):

    def create_inputs_schema(self):
        return {
            "table_input": {
                "type": "table"
            }
        }

    def create_outputs_schema(self):
        return {
            "table_output": {
                "type": "table"
            }
        }

    def process(self, inputs, outputs) -> None:
        pass
```

This module skeleton describes a *kiara* module that takes a dataset of type `table` as input (using `table_input` as input field name), and produces another table dataset as output (accordingly, using `table_output` as output field name). For your own modules, you'd probably use the field name `table` for both input and outputs, but in this tutorial we'll use the longer forms, to avoid any confusion.

On the next *kiara* run, the new module should be picked up by the `operation list` command:

{{ cli("kiara", "operation", "list", "tutorial_module", max_height=200, extra_env={"CONSOLE_WIDTH": "140", "KIARA_CONTEXT": "_my_kiara_module"}) }}

The id of the module was autogenerated from the full Python path of its class: `kiara_plugin.my_kiara_module.my_kiara_module.tutorial_module`.

### Module id and description

In most cases, we don't want such a long and unwieldy module name. We can assign our own, custom and meaningful id by setting the `_module_type_name` class attribute. In addition, we will want to add some documentation about the module and its functionality that is displayed to the user. For this, we use a normal Python doc string on the Python class body. For the purpose of this tutorial, we'll only add a single sentence, but in most cases you'll want to have a multi-paragraph markdown text here. So, taking all that into account, edit the module code to include:

```python
...
...
class TutorialModule(KiaraModule):
    """Filter a table."""

    _module_type_name = "filter.table"

    def create_inputs_schema(self):
        return {
...
...
```

The output for our new module in the operation list is much prettier now:

{{ cli("kiara", "operation", "list", "filter", max_height=200, extra_env={"CONSOLE_WIDTH": "140", "KIARA_CONTEXT": "_my_kiara_module"}) }}

We can also let *kiara* tell us about what it knows about the operation itself:

{{ cli("kiara", "operation", "explain", "filter.table", max_height=200, extra_env={"CONSOLE_WIDTH": "140", "KIARA_CONTEXT": "_my_kiara_module"}) }}

### Input/output field documentation

As you can see in the `explain` output above, the information to the user is still a bit sparse. In most cases, we'll want to have some information about the input(s) the user is supposed to provide. Same for what the outputs actually mean. In both cases, we can add a `doc` attribute to each input and output field.

```python
    ...
    ...
    def create_inputs_schema(self):
        return {
            "table_input": {
                "type": "table",
                "doc": "The table to filter."
            }
        }

    def create_outputs_schema(self):
        return {
            "table_output": {
                "type": "table",
                "doc": "The filtered table."
            }
        }
    ...
    ...
```

Run the `explain` command again, to check what *kiara* thinks of our module now:

{{ cli("kiara", "operation", "explain", "filter.table_2", fake_command="kiara operation explain filter.table", max_height=200, extra_env={"CONSOLE_WIDTH": "140", "KIARA_CONTEXT": "_my_kiara_module"}) }}

### Processing the inputs

Specifying the inputs (and outputs) is an important part of designing your module, it's basically the modules' 'public API', and you want to avoid changing it (too much; or at all) as your module evolves over time. But of course, the actual processing is where the interesting stuff happens. In *kiara*, that is the `process` method of every module. The arguments to this method are called `inputs` and `outputs`, which are basically dicts that use the field names specified in the `create_inputs_schema` / `create_outputs_schema` as keys, and Python objects of class [Value][kiara.models.values.value.Value] as values.

One thing to understand is that a `Value` object is not the same as the actual data. Instead, it's a reference to it (a means to retrieve it), and it also contains metadata about it's provenance (pedigree/lineage) and other properties.

This is the signature of the `process` method, including type hints (which we will omit after this):

```python
from kiara.models.values.value import ValueMap, ValueMapWritable

    def process(inputs: ValueMap, outputs: ValueMapWritable):
        ...
        ...
```

The `inputs` and `outputs` arguments to the `process` method are of type [ValueMap][kiara.models.values.value.ValueMap], the two main methods to access input data are:

- `inputs.get_value_obj([field_name])`: retrieve the (wrapper) `Value` object for a field
- `inputs.get_value_data([field_name])`: retrieve the data object for a field

In addition, you can retrieve the data object via the value wrapper:

```python
value = inputs.get_value_obj("field_name")
data = value.data
```
The class/type of the data depends on the data type of the value, so you'll have to consult the documentation about what to expect. TODO: expand on this, with a bit of example code/cli commands

The important methods to set an output is:

- `outputs.set_value(field_name, result_data)`: set a single output field
- `outputs.set_values(field_name_1=result_data_1, field_name_2=result_data_2, ...)`: set multiple result values at once

All that out of the way, let's get started implementing our table filter. We'll do it in stages, so hopefully we can cover all the important aspects in this tutorial in a way that makes intuitive sense.

To that end, let's write some code that does ...nothing. Our first iteration of our module will take the input table, and immediately set it as output:

```python
def process(inputs, outputs):

    table_obj = inputs.get_value_obj("table_input")

    # some debug output is usually useful while developing. Something like:
    print(f"Filter module, table input: {table_obj}")
    print("Table data:")
    print(table_obj.data)

    outputs.set_value("table_output", table_obj)
```

If we `run` our module in this state, we should see our debug output, as well as the resulting table (which will be the unmodified input):

{{ cli("kiara", "run", "filter.table_2", "table_input=alias:journal_nodes_table", fake_command="kiara run filter.table table_input=alias:journal_nodes_table", max_height=200, extra_env={"CONSOLE_WIDTH": "140", "KIARA_CONTEXT": "_my_kiara_module"}) }}

Now it's time to drill a bit deeper into our input table, and figure out how to access the information it contains. *kiara* wraps data that shares some schema/structure into so-called 'data types'. You can access a list of the data types that are available in your current *kiara* environment with the `data-type list` sub-command:

{{ cli("kiara", "data-type", "list", max_height=200, extra_env={"CONSOLE_WIDTH": "140", "KIARA_CONTEXT": "_my_kiara_module"}) }}

To find out more about a specific data type, you can use `data-type explain`:

{{ cli("kiara", "data-type", "explain", "table", max_height=200, extra_env={"CONSOLE_WIDTH": "140", "KIARA_CONTEXT": "_my_kiara_module"}) }}

Reading this, and following some of the links included. shows us that we can retrive the table data as a Pandas dataframe using the `to_pandas()` method. As the documentation states, this loads the whole data into memory, which is something we should try to avoid, but in a lot of cases (esp. if we are dealing with sub-hundreds-of-megabytes-sized data) it's a perfectly acceptable approach. So, let's do this and use our existing knowledge of Pandas, and retrieve a list of column names from the table the user provided, print out that information debug-style, using print:

```python
def process(self, inputs, outputs) -> None:

    table_obj = inputs.get_value_obj("table_input")

    print(f"Filter module, table input value: {table_obj}")
    print(f"Table data instance: {table_obj.data}")

    pandas_df = table_obj.data.to_pandas()
    print(f"Column names: {pandas_df.columns}")

    outputs.set_value("table_output", table_obj)
```

Again, let's run and see what's what (this time surpressing the result output we don't need right now, using `--output silent`):

{{ cli("kiara", "run", "--output", "silent", "filter.table_3", "table_input=alias:journal_nodes_table", fake_command="kiara run --output silent filter.table table_input=alias:journal_nodes_table", max_height=200, extra_env={"CONSOLE_WIDTH": "140", "KIARA_CONTEXT": "_my_kiara_module"}) }}

Ok, now we filter. Initially, let's say our module accepts only tables that contain a 'City' column, and returns all rows that have 'Berlin' as a value there:

```python
def process(self, inputs, outputs) -> None:

    from kiara.exceptions import KiaraProcessingException

    table_obj = inputs.get_value_obj("table_input")
    pandas_df = table_obj.data.to_pandas()

    column_names = pandas_df.columns
    if "City" not in column_names:
        raise KiaraProcessingException("Invalid table, does not contain a column named 'City'.")

    berlin_df = pandas_df.loc[pandas_df['City'] == "Berlin"]
    outputs.set_value("table_output", berlin_df)
```

And again, we run our module using our example dataset, and now we actually get something that is filtered:

{{ cli("kiara", "run", "filter.table_4", "table_input=alias:journal_nodes_table", fake_command="kiara run filter.table table_input=alias:journal_nodes_table", max_height=200, extra_env={"CONSOLE_WIDTH": "140", "KIARA_CONTEXT": "_my_kiara_module"}) }}

Of course, a module like this is only of very limited value, because the tables it accepts as inputs must contain a column named 'City', and it only filters out a hardcoded string. Ideally, we'd want the user to provide both inputs, along with the table to filter. Let's add those module inputs, and adjust the processing method accordingly:

```python
    def create_inputs_schema(self):
        return {
            "table_input": {
                "type": "table",
                "doc": "The table to filter."
            },
            "column_name": {
                "type": "string",
                "doc": "The column containing the element to use as filter.",
                "default": "City"
            },
            "filter_string": {
                "type": "string",
                "doc": "The string to use as filter."
            }
        }

    def process(self, inputs, outputs) -> None:

        from kiara.exceptions import KiaraProcessingException

        table_obj = inputs.get_value_obj("table_input")
        column_name = inputs.get_value_data("column_name")
        filter_string = inputs.get_value_data("filter_string")

        pandas_df = table_obj.data.to_pandas()

        column_names = pandas_df.columns
        if column_name not in column_names:
            raise KiaraProcessingException(f"Invalid table, does not contain a column named '{column_name}'. Available column names: {', '.join(column_names)}.")

        berlin_df = pandas_df.loc[pandas_df[column_name] == filter_string]
        outputs.set_value("table_output", berlin_df)
```

In this example, I've used a default value for the `column_name` input ('City'). This propably doesn't make a whole lot of sense, but it shows how to set defaults for input fields, which in a lot of cases makes sense. We can try to run this command using a missing `filter_string` argument, which shows off nicely what the *kiara* command-line interface has to say about something like this:

{{ cli("kiara", "run", "filter.table_5", "table_input=alias:journal_nodes_table", fail_ok=true, fake_command="kiara run filter.table table_input=alias:journal_nodes_table", max_height=200, extra_env={"CONSOLE_WIDTH": "80", "KIARA_CONTEXT": "_my_kiara_module"}) }}

As you can see, *kiara* complains about the missing input, but has used 'City' as default for the missing `column_name` input, and therefor is ok with the user not providing this. Ok, one more time, let's look for 'Amsterdam':

{{ cli("kiara", "run", "filter.table_5", "table_input=alias:journal_nodes_table", "filter_string=Amsterdam", fake_command="kiara run filter.table table_input=alias:journal_nodes_table filter_string=Amsterdam", max_height=200, extra_env={"CONSOLE_WIDTH": "140", "KIARA_CONTEXT": "_my_kiara_module"}) }}

This should give you a good basis to work on your own *kiara* module(s). Stay tuned for part II of this tutorial!
