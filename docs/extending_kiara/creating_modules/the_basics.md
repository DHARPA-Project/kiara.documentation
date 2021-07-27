---
title: The basics
---

# Writing your own *kiara* module - the basics

## Preparation

### Setting up development environment

For this tutorial, we'll use the [kiara_modules.playground](https://github.com/DHARPA-Project/kiara_modules.playground) repository as our development environment.

To get going, follow the instructions to prepare a development environment in the README, then create a Python module with your own name under ``src/kiara_modules/playground`` (similar to the existing ones).

You can put your code in the resulting ``__init__.py`` file, or create an entirely new Python module within, whatever you prefer. The module names and a few other paths in the following might differ slightly from what you will see when following along, but I trust you'll nonetheless figure out the right thing to do... If not, contact me and let me know how to improve this guide!

### Check out the '*kiara* getting started guide'

If you haven't already, it would make sense for you to go through the [*kiara* getting started guide](../../../usage/getting_started/). This will give you a good overview of the relevant *kiara* features, and how the module(s) you are going to write fits in.

### Pre-loading the example table we are going to use

As input data for this tutorial, we'll use [this very small csv file](https://github.com/DHARPA-Project/kiara_documentation/blob/develop/examples/data/writing_module_tutorial/data_1.csv):

{{ inline_file_as_codeblock('examples/data/writing_module_tutorial/data_1.csv', format='csv') }}

Download this file, and import it with kiara like so:

{{ cli("kiara", "run", "table.import.from_local_file", "path=examples/data/writing_module_tutorial/data_1.csv", "aliases=tutorial_data_1", max_height=240) }}

From now on, we'll be able to use this as input by specifying ``value:tutorial_data_1``.

## The basics

To explain the few absolute necessary things about *kiara* modules, let's write a very simple module that can filter a table by date. A *kiara* module is a Python class that extends the [``KiaraModule``](https://dharpa.org/kiara/api_reference/kiara.module/#kiara.module.KiaraModule) base class. You don't necessarily need to understand how classes and inheritance work in Python to be able to create your own module, all you really need to do is create a class structure that implements 3 methods. You can copy the following code into your own Python file in the playground, to get started:

```python
from kiara import KiaraModule

class MyFirstModule(KiaraModule):

    def create_input_schema(self):
        pass

    def create_output_schema(self):
        pass

    def process(self, inputs, outputs) -> None:
        pass
```

Execute a ``kiara module list`` command, and you should already see your module in the list of available ones:

```console
> kiara module list
  ...
  ...
  onboard.folder                          Import (copy) a folder and its metadata into the internal data store.│                                                                                                                                                                               │
  playground.lena.graph_components        -- n/a --
  playground.markus.my_first     -- n/a --
  playground.sandbox.example              A very simple example module; concatenate two strings.
  ...
  ...
```

This would (obviously) fail if we tried to run it, but it's good that *kiara* knows about it already, at least. As you can see, *kiara* tried to come up with a good alias for the module, based on the class name. It also sorted the module into a namespace (`playground.markus`) automaticaly, based on its location and package it is contained in. Which is fine, but, obviously, 'my_first' is not all that descriptive. So, let's give *kiara* a hint and tell it what better name to use:

```python
...
...
class MyFirstModule(KiaraModule):

    _module_type_name = "filter_table_by_date"

    def create_input_schema(self):
       ...
       ...
```

What we did here was to give the class itself a new attribute ``_module_type_name``. *kiara* knows to check for its existence, and will use it as the last part of the module id if it finds it set. Check the output of ``kiara module list`` again. Name changed? Cool. Coocoocool. We could try to run this module with ``kiara run playground.markus.filter_table_by_date`` already, but it'd only throw an error since it is still missing implementation.

The base ``KiaraModule`` class is what is called an 'abstract base class', which does not have to concern you overly much, apart from that this means there are a few methods missing for it to be functional. You can see the names of the methods in the copied code above, so let's go through them in order:

### method: ```create_input_schema(self)```

The result of this method tells *kiara* what inputs the module expects: their names, and what types they are. In our case, we said we wanted to filter a table by date, so obviously we need one input that's a table, and one that is date. *kiara* comes with a few data types by default, and you can get a list of available ones via:

{{ cli("kiara", "type", "list", max_height=240) }}

It looks like we are in luck, and there is both a 'table' and 'date' data type already. At the moment there is no command yet so you can get more information about those types (there will be, later), so for now let me tell you that the 'table' type is represented internally by the [Apache Arrow Table class](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html#pyarrow.Table) class, and date by [datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime). If we look up the [Python API doc for this method](https://dharpa.org/kiara/api_reference/kiara.module/#kiara.module.KiaraModule.create_input_schema) we can see that we are expected to return a dictionary with strings as keys, and other dictionaries (describing the input) as values (or something of type `ValueSchema`, but we can ignore this for now).

So, for our case, the implementation of that method would look like this:

```python
def create_input_schema(self):
    return {
        "table_input": {
            "type": "table",
            "doc": "The table that will be filtered."
        },
        "date": {
            "type": "date",
            "doc": "The minimum date, earlier dates will be filtered out."
        }
    }
```

### method: ```create_output_schema(self)```

The format of the result of this method is very similar to the above. The (only) result of our module will be another table. So, here's what that will look like:

```python
def create_output_schema(self):
    return {
        "table_output": {
            "type": "table",
            "doc": "The filtered table."
        }
    }
```

### Interlude: displaying the information *kiara* has about our module, so far

After adding the code for the input and output schema, we basically defined the interface of our module. Such an interface is important, because it is how other people will interact with it. *kiara* can display this interface, along with other important bits and pieces with the ``module explain-instance`` sub-command:

{{ cli("kiara", "module", "explain-instance", "kiara_documentation.writing_modules.filter_table_by_date", max_height=240, fake_command="kiara module explain-instance playground.markus.filter_table_by_date") }}

As you can see, *kiara* picked up your implementation, and converted it to an auto-generated documentation of the module. We can also 'run' the module without any input. In that case, *kiara* will give us a brief usage hint that tells the user which inputs are needed:

{{ cli("kiara", "run", "kiara_documentation.writing_modules.filter_table_by_date", max_height=240, fake_command="kiara run playground.markus.filter_table_by_date") }}

### method: ```process```

Now, onto implementing the actual meat of our *kiara* module, the ``process`` function. This function in its most basic form takes two arguments: ``inputs``, and ``outputs``. Both are objects of the [``ValueSet``](https://dharpa.org/kiara/api_reference/kiara.data.values/#kiara.data.values.ValueSet) class, which is basically a Python dictionary with the field_names as keys, and the actual values as, well ...values.

There is one thing in all of this that is a bit unintuitive compared to how you would normally expect to program something like this (well, I'm sure there is more, but this is the most crucial): *kiara* tries to avoid handling the actual data (bytes/data objects) as much as possible, and only accesses them at the last possible moment. This is a strategy to keep memory utilization and data transfer as close to a minimum as possible. It would not make much sense to introduce something like this for workflows and processes that only deal with small(-ish) datasets, but we can't rely on always having small datasets and we'd like to be prepared for more demanding computations. So our design has to cater for the worst case, rather than the best. What this means is that as a module developer you have to go through one extra step to get to the actual data, if you need it. Typically, this step will look like this:

```python
def process(inputs, outputs):

    table_obj = inputs.get_value_data("table_input")

    outputs.set_value("table_output", table_obj)
```

What we have done here is to request the table data (the 'table_input' key in ``create_input_schema``) from *kiara*, and then set that table directly as the output value (the name 'table_output' in this case is the key of the result in ``create_output_schema``). So our module does absolutely nothing, it only uses the input it received as output, and returns that unchanged. We can try that out by running the module again, this time with inputs (we'll just use random input for the 'date' for now):

{{ cli("kiara", "run", "kiara_documentation.writing_modules.filter_table_by_date_2", "table_input=value:tutorial_data_1", "date=1977-01-01", max_height=240, fake_command="kiara run playground.markus.filter_table_by_date table_input=value:tutorial_data_1 date=1977-01-01") }}

So, we get back exactly the data we put in. Now we just have to somehow filter it. For that, first we need to retrieve the 'date' input, and we can do that the same way we did with 'table_input'. For debugging and development purposes, I like to just print some of those inputs or intermediate results in the module code while I work on it. Something like:

```python
def process(self, inputs, outputs):

    table_obj = inputs.get_value_data("table_input")
    date_input = inputs.get_value_data("date")

    print("------")
    print(f"HELLO FROM INSIDE THE MODULE, THIS IS OUR DATE: {date_input}")
    print("------")

    outputs.set_value("table_output", table_obj)
```

Let's run (with the ``--output=silent`` option, because for now we are not interested in the result -- we know it's the same as the input):

{{ cli("kiara", "run", "--output=silent", "kiara_documentation.writing_modules.filter_table_by_date_3", "table_input=value:tutorial_data_1", "date=1977-01-01", max_height=240, fake_command="kiara run --output=silent playground.markus.filter_table_by_date table_input=value:tutorial_data_1 date=1977-01-01") }}

### Filter the table, using Pandas

Ok. Now. Actual filtering! Later, I'll show you a few options to filter a table, but lets start with a pandas based approach, since Pandas is probably something a lot of people are familar with. One nice thing about Apache Arrow ``Table`` objects is that they let us create Pandas dataframes from them super easy, all we need to do is call `[table].to_pandas()`. And, creating an Arrow table from a dataframe is similarly simple (as you'll see below). So, here is a first implementation of the filtering code:

```python
def process(self, inputs, outputs):

    table_obj = inputs.get_value_data("table_input")
    date_input = inputs.get_value_data("date")

    df = table_obj.to_pandas()

    after_date = df[df["birthday"] >= date_input.date()]

    import pyarrow as pa
    result_table = pa.Table.from_pandas(after_date, preserve_index=False)

    outputs.set_value("table_output", result_table)
```

Again, let's run our thing, and look at the output:

{{ cli("kiara", "run", "kiara_documentation.writing_modules.filter_table_by_date_4", "table_input=value:tutorial_data_1", "date=1977-01-01", max_height=240, fake_command="kiara run playground.markus.filter_table_by_date table_input=value:tutorial_data_1 date=1977-01-01") }}

And that was that! Your first *kiara* module!

Obviously, this is simplified to the point of being useless in practice. For example, we can't really rely on the 'birthday' column to always be there. And we also might want to have an option to filter later dates instead of earlier ones. Or a time range...

I'll lay out some of those problems, and their solutions in the next chapter, but that still has to be written, and I'm not sure when I'll get to it.

Still, I hope this first bit gives you enough information to get started on your first module. Ping me if you need any help, or create an issue in the [kiara_documentation git repo](https://github.com/DHARPA-Project/kiara_documentation) if you feel some of the documentation is unclear, or have other suggestions or ideas for improvements.
