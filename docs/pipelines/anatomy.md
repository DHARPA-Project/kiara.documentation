---
title: Anatomy of a pipeline
---

# The anatomy of a *kiara* pipeline

### Example: `nand` pipeline

In *kiara*, pipelines can be written in JSON or YAML format. For the purpose of this document we'll use a YAML description (as it's slightly easier to read)
of a pipeline that describes a logic 'nand' operation.

'nand' is as simple as workflows go, it consists of two operations chained one after the other: 'and' to compute an output that is only true if both its inputs
are true, and a 'not' operation that negates that output. Later on we'll show more topic-relevant -- and complex -- examples, but for the purpose of describing
the format of a pipeline description, this will helpfully not add extra complications.

``` yaml
module_type_name: nand # (1)
steps:  # (2)
  - module_type: logic.and # (3)
    step_id: and_operation # (4)
  - module_type: logic.not
    step_id: negate_and
    input_links: # (5)
      a: and_operation.y # (6)
input_aliases: # (7)
  and_operation__a: a
  and_operation__b: b
output_aliases: # (8)
  negate_and__y: y
```

1. Optional, a string without any special characters, except '_' (underscore). If not provided the name of the file is used to auto-generate a module type name.
2. Required, a non-empty list of dictionaries. The order of the modules is not relevant, but it is good practice to put them in the order they are executed, for easier reading.
3. Required, the name of the module or operation to use (check available modules with `kiara module list` and operations with `kiara operation list`)
4. Required, the name of the step. In a lot of simple pipelines you can re-use the module name. The value for this attribute must be unique within the pipeline, so you can't have two steps with the same `step_id`. Ideally, pick a short and descriptive name (not `a`, `b`, `step_one` or so).
5. Required if one of the inputs of this step is connected to another steps output. The value of this filed is a dictionary with the name of the step input as a key, and the connected output as a value, in the form: `[step_id].[output_name]`.
6. In this case we connect the (only) `a` input with the `y` output of our and operation. We can get the output/input names of the respective operations with the commands: `kiara operation explain logic.not` nad `kiara operation explain logic.and`.
7. Optional, a dictionary with the auto generated pipeline input name (format: `[step_id]__[input_name]` -- two underscores!) as key, and the desired pipeline input field name as value. If not specified, the auto-generated name will be used.
8. Optional, a dictionary with the auto generated pipeline output name (format: `[step_id]__[output_name]` -- two underscores!) as key, and the desired pipeline output field name as value. If not specified, the auto-generated name will be used.

Click on the numbers for more details on any of the attributes.

At any stage of your pipeline assembly process you can run either one of the following commands to get some feedback of what *kiara* thinks of your pipeline so far. This will only work if the pipeline format is correct though (meaning valid JSON or YAML, and no missing required attributes):

``` console
# get a general usage overview of your pipeline
> kiara operation explain <path_to_your_pipeline_file>

# get a more detailed overview of the internal structure of your pipeline
> kiara pipeline explain <path_to_your_pipeline_file>

# print the execution graph of the pipeline (requires additional dependency -- instructions will be in error message):
> kiara pipeline execution-graph <path_to_your_pipeline_file>

# print the data-flow graph of the pipeline (requires additional dependency -- instructions will be in error message):
> kiara pipeline data-flow-graph <path_to_your_pipeline_file>
```
