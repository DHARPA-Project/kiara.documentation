---
title: Operation types
---

*kiara* has a pluggable architecture that supports the creation and management of operations that are conceptually similar (or the same), with the only
difference being that they take inputs of different types.

As an example, imagine an operation that prints out a value in a human readable form (usually referred to as 'pretty printing'). The code to print out
a Python object differs, depending on the type of the object, as well as the target the value should be printed to.

If we assume the target to be the terminal, printing scalars like `string`, `integer` and `boolean` is easy, all you need
to do is `print(value)`. It becomes more tricky when the objects become more complex, though. Using `print` on a `table` (backed by Apache Arrow)
would for example yield:

```
pyarrow.Table
Id: int64
Label: string
JournalType: string
City: string
CountryNetworkTime: string
PresentDayCountry: string
Latitude: double
Longitude: double
Language: string
```

Which gives us some information about the table, but not enough to be usable for end-users. We'd want to see a preview of the actual
table data, similar to how Pandas dataframe objects are displayed in Jupyter: if the table is too
large to be printed in its entirety, we'd at least want to see the first and last few rows of the table, along with some
visual indication that there is more data that is not displayed, and ideally row numbers so we can see how many rows there
are in total.

The reason for specific operation types to exist in *kiara* is that in a generic framework, we hardly ever know for sure which types
of data we'll encounter when offering UI components that allow the user to either view, or interact with data. Or apply transformations to.
If we had a way of indicating to *kiara* that, for a specific operation (like `pretty_print`) is available for the type of the data we are
currently holding, *kiara* could automatically choose that operation in a specific scenario, which would remove the need to prompt users
for trivial decisions (e.g. 'How do you want this data to be displayed?').

So, in this section we'll list the operation types that are available in *kiara*, and explain what each of them do, which data types
are supported, and how to extend them, add your own operations, as well as create new operation types if you find that there
is none that would support your use-case.

{% for op_type in get_kiara_context().operations.operation_types.values() %}
- [`{{ op_type.info.type_name }}`]({{ op_type.info.type_name }}): {{ op_type.info.documentation.description }}
{% endfor %}
