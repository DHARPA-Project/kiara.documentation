---
title: Assembling a pipeline
description: How to assemble multiple kiara modules into a pipeline
tags:
- tutorial
---

# Assembling a kiara pipeline

## Preparation

If you haven't already, it would make sense for you to go through the [*kiara* getting started guide](../../../usage/getting_started/), as well as [writing your own *kiara* module](../creating_modules/the_basics). We'll use the
development environment set-up from the latter guide, as well as the module created there as a step in our pipeline.

## Creating a pipeline

A *kiara* pipeline is a dict-like data structure that includes one or several processing steps (implemented by *kiara* operations), connected (or not) in a specific way so that some steps outputs feed into other steps' inputs.

### A single-step pipeline

The simplest pipeline contains a single operation, and is not use-full in any way, since it's easier to just `kiara run`
the operation directly. Nonetheless, below is how that would look like, we'll be using the module we created in the [writing your own *kiara* module](../creating_modules/the_basics) guide:

```yaml
steps:
  - module_type: filter.table
    step_id: filter_table_step
```

A pipeline step is a dictionary with 2 required keys (and some optional ones, which we'll cover later):

- **`module_type`**: the name of the module or operation that should be used.
- **`step_id`**: the name of the step, ideally a short, descriptive name of what the step does. It can't contain special characters except '_', and it must be unique within the pipeline.

An assembled pipeline has the same characteristics as a *kiara* module, and in fact is a perfectly valid operation, like any other one, and can be called the same way.

Create a new file `my_first_pipeline.yaml`, and copy and paste the above code into it. The, run the `operation explain` command against the file:

{{ cli("kiara", "operation", "explain", "examples/pipelines/tutorial_1.yaml", fake_command="kiara operation explain my_first_pipeline.yaml", extra_env={"CONSOLE_WIDTH": "140", "KIARA_CONTEXT": "_assembling_pipeline"}) }}

As you can see, *kiara* turned this (single-step) pipeline into an operation, and auto-generated some input- and output-fields, by assembling the step-id and step input-/output-field(s). Those long field names are a bit unwieldy, and we'll remedy that later, but for now let's just ignore that.

### Adding a second step

In the previous tutorial we pre-seeded the *kiara* data store with a csv file/tabular dataset, to help us with developing our table filter module. In this tutorial, we'll remove the requirement to do that, by adding a step to our pipeline that lets the user specify a path to a csv file, and import and convert that into a table value.

Previously, we've used the `import.table.from.csv_file` operation to import the csv file, and we can do the same now. Edit the pipeline file you created so it looks like the following:

```yaml
steps:
  - module_type: import.table.from.csv_file
    step_id: import_table_step
  - module_type: filter.table_5
    step_id: filter_table_step
    input_links:
      table_input: import_table_step.table
```

What we did here:

- add a new step with the id `import_table_step`, which will execute the `import.table.from.csv_file` operation
- leave our filter step in place, but connect the `table_input` input of this steps operation to the `table` output field of the `import_table_step` operation

We can ask *kiara* again about what it thinks of this new pipeline/operation:

{{ cli("kiara", "operation", "explain", "examples/pipelines/tutorial_2.yaml", fake_command="kiara operation explain my_first_pipeline.yaml", extra_env={"CONSOLE_WIDTH": "140", "KIARA_CONTEXT": "_assembling_pipeline"}) }}

As you can see, the previously existing input with the field name `filter_table_step__table_input` (type: table) is gone now, replaced by a new one, with the field name `import_table_step__path` (type: string). The other two inputs remain the same (since we did not connect any output to them).

### Side-note: visualizing the pipeline

We can let *kiara* visualize our pipeline at each step in the development process. This is quite useful, as it can serve as a visual aid to debug and assemble pipelines and their steps.

If you want to do this in your own environment, you need to have Java installed, as well as an additional Python dependency in your virtual- or conda-environment:

```
pip install 'git+https://github.com/cosminbasca/asciinet.git#egg=asciinet&subdirectory=pyasciinet'
```

Currently, commands exist to print a pipeline as graph on the command-line:

- `kiara pipeline execution-graph <pipeline_file>`: display the pipeline steps in the order they will be executed.
- `kiara pipeline data-flow-graph <pipeline_file>`: display the the connections of inputs/outputs as well as processing steps.

As an example, let's look at the execution graph of our current pipeline:

{{ cli("kiara", "pipeline", "execution-graph", "examples/pipelines/tutorial_2.yaml", fake_command="kiara pipeline execution-graph my_first_pipeline.yaml", extra_env={"CONSOLE_WIDTH": "140", "KIARA_CONTEXT": "_assembling_pipeline"}) }}

### Adjusting the input-/output-field names

We could run our pipeline as is, but let's adjust its input- and output field names first, to make it nicer to use.
To do that we can to add one or both of the following keys to our pipeline description:

- `input_aliases`: a mapping of pipeline inputs to more user-friendly names
- `output_aliases`: a mapping of pipeline outputs to more user-friendly names

Lets start with our inputs. Add the following to your pipeline file:

```yaml
input_aliases:
    import_table_step.path: csv_file_path
    filter_table_step.column_name: column_name
    filter_table_step.filter_string: filter_string
```

This is basically just a rename of one (or several, or all) pipeline-input-fields, to shorter names. If you specify the same value for several keys, then the user input for those fields will be re-used for all the keys that have that value (we'll cover that in a later tutorial).

Now let's do our outputs:

```yaml
output_aliases:
    filter_table_step.table_output: filtered_table
```

Output aliases work a bit different to input aliases: for the latter, if we don't specify an input field, *kiara* will just use the auto-generated name. For outputs aliases, if we don't specify an alias, *kiara* will ignore that output, and not display it to the user. In our case, we are not really interested in the intermediate outputs of the first step, so we only add the `filtered_table` alias that represents our final, filtered result.

Lets see what *kiara* has to say about the pipelines 'API' now:

{{ cli("kiara", "operation", "explain", "examples/pipelines/tutorial_3.yaml", fake_command="kiara operation explain my_first_pipeline.yaml", extra_env={"CONSOLE_WIDTH": "100", "KIARA_CONTEXT": "_assembling_pipeline"}) }}

Much nicer!

### Run the pipeline

Now, all that is left to do is run the pipeline:

{{ cli("kiara", "run", "examples/pipelines/tutorial_3.yaml", "csv_file_path=examples/data/journals/JournalNodes1902.csv", "filter_string=Amsterdam", "column_name=City", fake_command="kiara run my_first_pipeline.yaml csv_file_path=examples/data/journals/JournalNodes1902.csv filter_string=Amsterdam column_name=City", extra_env={"CONSOLE_WIDTH": "140", "KIARA_CONTEXT": "_assembling_pipeline"}) }}
