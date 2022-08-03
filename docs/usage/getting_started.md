---
description: Getting started with kiara.
tags:
- tutorial
---

# Getting started

This guide walks through some of the important (and some of the lesser important) features of *kiara*, the goal is to introduce
new users to the overall framework, so they can get a feeling for what it can do, and whether it might be useful for their
own usage scenarios.

## Setting up kiara

In order to use *kiara*, we'll need to install it into a Python virtual (or conda-) environment, along all the plugins we might want to use. For the purpose of this tutorial, we'll use [conda](https://docs.conda.io/en/latest/) to create such an environment, but you can of course use a 'normal' virtualenv if you prefer. How to install *conda* itself is out of scope of this tutorial, but you should not have problems finding instructions online.

One simple way is to install the [Anaconda (individual edition)](https://docs.anaconda.com/anaconda/install/index.html), then use the Anaconda navigator to create a new environment, install the 'git' package in it (if your system does not already have it), and use the 'Open Terminal' option of that environment to start up a terminal that has that virtual-/conda-environment already activated.


Here's how to create the environment, activate it, then install the necessary dependencies (assuming conda is installed):

```console
conda create -n kiara_tutorial python=3.9
conda activate kiara_tutorial
conda install -c conda-forge mamba
mamba install -c conda-forge -c dharpa kiara kiara_plugin.core_types kiara_plugin.tabular kiara_plugin.network_analysis
```

!!! note
    We are using [mamba](https://github.com/mamba-org/mamba) as our package manager here, instead of 'pure' conda. This is optional, but recommended since it makes things a lot faster.


## Getting some example data

For this tutorial, we'll need some example data, so we can use *kiara* against it. We've prepared a git repository for that purpose:

```console
git clone https://github.com/DHARPA-Project/kiara.examples.git
cd kiara.examples
```

Specifically, here we'll be using two CSV files that were created by my colleague [Lena Jaskov](https://github.com/yaslena): [files](https://github.com/DHARPA-Project/kiara.examples/tree/main/examples/data/journals)

The files contain information about connection (edges) between medical journals (``JournalEdges1902.csv``), as well as additional metadata for the journals themselves (``JournalNodes1902.csv``). We'll use that data to create table and graph structures with *kiara*.


## Checking for available operations

First, let's have a look which operations are available, and what we can do with them:

{{ cli("kiara", "operation", "list", max_height=320, extra_env={"CONSOLE_WIDTH": "140"}) }}

!!! note
    In this guide we'll use the term *operation* to indicate an entity that transforms data in some way or form. *kiara*
    also has the concept of *module* (the differences are explained in more detail [here](../concepts/index.md)), and in most
    cases the meaning of '*module*' and '*operation*' is roughly the same. Especially in the context of this 'Getting started'
    guide. Nonetheless, keep in mind that technically both terms refer to different things.

## Importing data, and creating a table

Tables are arguably the most used (and useful) data structures in data science and data engineering. They come in different
forms; some people call them spreadsheets, or dataframes. We're not fancy, so we won't do that: we'll call them tables.

A depressingly large amount of (tabular) data comes in CSV files, which is why we'll use one as an example here. Specifically, we will
use [``JournalNodes1902.csv``](https://github.com/DHARPA-Project/kiara.examples/blob/main/examples/data/journals/JournalNodes1902.csv). As stated above, this file contains information about historical medical
journals (name, type, where it was from, etc.), and we'll later use it as the table which will provide node information in a network graph. We want to convert this file into a 'proper' table structure, because
that will make subsequent processing faster, and also simpler in a lot of cases. 'Proper', in this case means we'll convert it into a better format for internal use, for example containing information about the data type in each column, among other things.

### Finding the right command, and how to use it

*kiara* likes its data 'onboarded' (or: 'imported'), meaning it prefers to work with data that was imported into its internal data store. This effectively duplicates a file on a users filesystem (and depending on the filesystem used this could mean doubling the hard-disk space required for that particular dataset). The reason behind this preference is that this ensures the data won't be modified by an external application after import. This enables *kiara* to employ some techniques to save memory, hard-disk space as well as cpu-resources down the line.

So, in most cases, the first thing you (as a user) want to do is 'import' the source data you want to work with. So, let's run the `operation list` command again, but let's filter using the term 'import':

{{ cli("kiara", "operation", "list", "import", max_height=320, extra_env={"CONSOLE_WIDTH": "140"}) }}


#### Importing the 'raw' file

After looking at the ``kiara operation list`` output, it looks like the ``import.file`` module might be just what we need (to be honest, `import.table.from.csv_file` is what we'd really use if we weren't stuck in this getting-started guide, but doing that would skip over a few important basics that are worth understanding).

*kiara* has the [``run``](../running_operations) sub-command, which is used to execute operations. If we only provide a module name, and not any input, this command will tell us what it expects:

{{ cli("kiara", "run", "import.file", fail_ok=True) }}

As makes obvious sense, we need to provide a ``path`` input, of type ``string``, letting *kiara* know where to pick up the file. The *kiara* command-line interface can
take complex inputs like dictionaries, but fortunately this is not necessary here. If you ever come into a situation where you need that, check out [this section](../..//usage/#complex-inputs).

For simple inputs like string-type things, all we need to do is provide the input name, followed by '=' and the value itself:

{{ cli("kiara", "run", "import.file", "path=examples/data/journals/JournalNodes1902.csv", max_height=340, extra_env={"KIARA_CONTEXT": "_getting_started"}) }}

As you can see from the terminal output, this produced one piece of output data: `file` (referring to the imported file), and it displays a preview of the file in question for us. By itself, this doesn't do anything yet, it just reads the file and then stops. What we want in this case is to 'save' the file, so we can refer to it again later. The process of 'saving' a value in *kiara* persists the file (rather: it's content and some metadata) into the *kiara* data store, giving it an internal unique id (string), and allows the user to 'tag' the value with one or multiple aliases. Aliases are names that are meaningful to the user, in order to make it easy to refer to datasets later on.

*kiara* supports saving any of the output values of a `kiara run` command via the `--save` flag. This `--save` parameter takes a single string as argument, and can be used in two ways:

- if you want to save all output fields of a `run` you can just provide a single string (for example `imported_journal_csv`) as the parameter. In this case, *kiara* will store all result items with an auto-generated alias in the form of `[save_argument].[field_name]`. In our case this would result in one item being store in the data store, with the alias `imported_journal_csv.file`.
- if you want to save only a subset of result values, or want to have more control about the aliases those results get, you can use the `--save` parameter for every field you want to persist. In this case the argument to `--save` must be in the form of: `[field_name]=[alias]`. You can use the `--save` parameter multiple times, with different field names.

In our case, lets opt for the second option:

{{ cli("kiara", "run", "--save", "file=journal_nodes_file", "import.file", "path=examples/data/journals/JournalNodes1902.csv", max_height=340, extra_env={"KIARA_CONTEXT": "_getting_started"}) }}

#### Checking the data store

To check whether that worked, we can list all of our items in the data store, and see if the one we just created is in there:

{{ cli("kiara", "data", "list", cache_key="1st_run_data_list", extra_env={"KIARA_CONTEXT": "_getting_started"}) }}

All right! Looks like this worked.

#### Creating a table from an imported CSV file

CSV files are usually not much use by themselves, in most cases we want to create a table-like structure from them, so we can efficiently query the data. This usually also makes sure that the structure and format of the file is valid.

Let's ask kiara what 'create' related operations it has available:

{{ cli("kiara", "operation", "list", "create", extra_env={"CONSOLE_WIDTH": "120"}) }}

Righto, looks like `create.table.from.csv_file` might be our ticket! Let's see what it does:

{{ cli("kiara", "operation", "explain", "create.table.from.csv_file", max_height=320) }}

So, it needs an input `csv_file` of type `file`, and will return a 'table'-named output of type, well ... `table`. Looks good. Here is how we run this:

{{ cli("kiara", "run", "create.table.from.csv_file", "csv_file=alias:journal_nodes_file", max_height=240, extra_env={"KIARA_CONTEXT": "_getting_started", "CONSOLE_WIDTH": "200"}) }}

!!! note
    In this example we pre-pend the right side of the `csv_file=` argument with `alias:`. This is necessary to make it clear to *kiara* that we mean
    a dataset that lives in its data store, and we want to refer to it via its alias. Otherwise, *kiara* would have just interpreted the input as a string, and since that is of the wrong input type
    (we needed a table), it would have thrown an error.

That output looks good, right? Much more table-y then before. Only thing is: we want to again 'save' this output, so we can use it later directly. No big deal, just like last time:

{{ cli("kiara", "run", "--output", "silent", "--save", "table=journal_nodes_table", "create.table.from.csv_file", "csv_file=alias:journal_nodes_file", extra_env={"KIARA_CONTEXT": "_getting_started"}) }}

!!! note
    Here we use the `--output silent` command line option to supress any output of values. We've seen this already in the
    last invocation of this command. *kiara* will still tell us the id of the value it just saved.

#### Checking the data store, again

Now, let's look again at the content of the *kiara* data store:

{{ cli("kiara", "data", "list", cache_key="2nd_run_data_list", extra_env={"KIARA_CONTEXT": "_getting_started"}) }}

As you can see, there are 2 items now: one `file`, and one `table`. If you ever want to get more details about any of the items in the data store, you can use one of those commands:

##### Display information about the data: `kiara data explain`

{{ cli("kiara", "data", "explain", "alias:journal_nodes_table", max_height=300, extra_env={"KIARA_CONTEXT": "_getting_started"}) }}

This command prints out the metadata *kiara* has stored about a value item. This commands supports displaying several internally important metadata details of stored datasets, check out the available options with ``kiara data explain --help``. One option that is particularly interesting is the `-p` one, which displays all the metadata properties *kiara* has collected about a value.

##### Display the data itself: `kiara data load`

{{ cli("kiara", "data", "load", "-s", "alias:journal_nodes_table", max_height=240, extra_env={"KIARA_CONTEXT": "_getting_started", "CONSOLE_WIDTH": "200"}) }}

!!! note
    If you omit the `-s` flag, this command will let you browse the table (or any other supported data type) interactively, similar to a pager application.

This command loads the actual data, and prints out its content (or a representation of it that makes sense in a terminal-context).

## Querying the table data

This section is a bit more advanced, so you can skip it if you want. It's just to show an example of what can be done with
a stored table data item.

We'll be using the [SQL](https://en.wikipedia.org/wiki/SQL) query language to find the names and types of all journals from Berlin. The query for this is:

```sql
select Label, JournalType from data where City='Berlin'
```

The *kiara* module we are going to use is called ``query.table``. Let's check again the parameters this module expects:

{{ cli("kiara", "run", "query.table", extra_env={"KIARA_CONTEXT": "_getting_started"}, fail_ok=True) }}

Aha. ``table``, and ``query`` are required. Good, we have both. In this example we'll use the data item we've stored as input for another workflow. That goes like this:

{{ cli("kiara", "run", "query.table", "table=alias:journal_nodes_table", "query=\"select Label, JournalType from data where City=\'Berlin\'\"", extra_env={"KIARA_CONTEXT": "_getting_started"}, max_height=240) }}

Note how we use the ``alias:``-prefix again here, to signify to *kiara* that what follows is indeed a reference to a dataset, and not a string...

### Saving the result of the query

As it is, the result of this query won't be saved anywhere. This might be fine for queries in exploratory-type situations. But in some cases
we might want to store the result of our work, similar to how we imported the original table in the first place. The ``kiara run`` command can do that, using the ``--save`` flag. It takes as argument a string. If that string contains a '=', it is interpreted as a key value pair where the key is the name of the field we want to save, and the value the alias we want to save it under. Here is how that goes:

{{ cli("kiara", "run", "query.table", "--output=silent", "--save", "query_result=berlin_journals", "table=alias:journal_nodes_table", "query=\"select Label, JournalType from data where City=\'Berlin\'\"", extra_env={"KIARA_CONTEXT": "_getting_started"}, max_height=240) }}

From looking at the output, it seems that saving our result has worked. We can make sure by letting *kiara* 'explain' to us the data that is stored under the alias 'berlin_journals'. This time, let's also display the result tables properties (by using the `--properties` flag:

{{ cli("kiara", "data", "explain", "--properties", "alias:berlin_journals", extra_env={"KIARA_CONTEXT": "_getting_started"}, max_height=240) }}


## Generating a network graph

Our goal for this tutorial is to create a network graph, and investigate its properties. Network graphs are usually created from
one or two pieces of data (both tabular in nature):

- *edges* (mandatory): information about what nodes exist, and if and how they are connected
- *nodes information* (optional): information about attributes of each node

!!! note
    In this tutorial we'll go through all the steps necessary to create a network graph object from two CSV files, one by one.
    This is a bit cumbersome, but it'll help you understand what actually happens. In a later tutorial we'll show how to create a *kiara* pipeline
    to combine all those steps into one.

### Importing edges data, creating a table item from it

We already have our nodes imported into kiara (with the alias `my_first_table`). Now we need to do the same for our edges. Similar to what we have done above, we want to import the file into
the *kiara* data store, and then convert it into a table. This time, let's just use a pre-pared (so-called) pipeline operation, which basically runs both operations in one, and feeds the right input(s) into the right input(s):

{{ cli("kiara", "operation", "explain", "import.table.from.csv_file", max_height=240) }}

So, let's see:

{{ cli("kiara", "run", "--save", "journal_edges", "import.table.from.csv_file", "path=examples/data/journals/JournalEdges1902.csv", extra_env={"KIARA_CONTEXT": "_getting_started"}, max_height=240 ) }}

!!! note
    Here we've used a simple string (without '=') with the `--save` option, and as you can see, *kiara* created two namespaced aliases for the result items.

At this stage we'll have two relevant tables in our store: `journal_edges.table`, and `journal_nodes_table` (note how both use different naming schemes due to us using the `--save` option differently in both cases):

{{ cli("kiara", "data", "list", cache_key="3rd_run_data_list", extra_env={"KIARA_CONTEXT": "_getting_started"}) }}

### Creating the graph

Now that we have the edges data in *kiara* in a useful format, we can create the graph object. The data type for graphs in *kiara* is called `network_data`, so let's check out all the operations *kiara* has to offer related to `network_data`:

{{ cli("kiara", "operation", "list", "network_data", extra_env={"KIARA_CONTEXT": "_getting_started", "CONSOLE_WIDTH": "180"}, max_height=320) }}

Hm, `create.network_data.from.tables` looks good, right? Let's see that operations interface:

{{ cli("kiara", "operation", "explain", "create.network_data.from.tables", extra_env={"KIARA_CONTEXT": "_getting_started", "CONSOLE_WIDTH": "120"}, max_height=320) }}

From this information we can assemble our command, using `alias:edges_table` as the main input, and saving it using the alias `journals_graph`. We can figure the values for the other inputs out be running `kiara data explain --properties journal_edges.table`, which will give us the edge column names, among other things (and, subsequently, `kiara data explain --properties journal_nodes_table. So, here goes nothing:

{{ cli("kiara", "run", "--save", "network_data=journals_graph", "create.network_data.from.tables", "edges=alias:journal_edges.table", "source_column_name=Source", "target_column_name=Target", "nodes=alias:journal_nodes_table", "id_column_name=Id", "label_column_name=Label", extra_env={"KIARA_CONTEXT": "_getting_started", "CONSOLE_WIDTH": "240"}, max_height=320) }}

To confirm our graph data is created, let's check the data store:

{{ cli("kiara", "data", "explain", "--properties", "alias:journals_graph", extra_env={"KIARA_CONTEXT": "_getting_started", "CONSOLE_WIDTH": "240"}, max_height=240) }}

All good. Also, check out the metadata *kiara* knows about the graph already.

### Side-note: investigating the graph value lineage

*kiara* keeps track of all the modules and inputs that went into producing a value, basically its entire ancestry. This is not the place to explain why, and how that can be
very powerful and useful. But if you are ever interested about what went into creating a particular value, you can do this with:

{{ cli("kiara", "data", "explain", "--lineage", "alias:journals_graph",  extra_env={"KIARA_CONTEXT": "_getting_started", "COLUMN_WIDTH": "140"}) }}

As you can see, this basically describes what we've done so far, to get to this stage. You could now do a `kiara explain data value:<value_id>` on each of the value ids you see here, if you were so inclined.

### More

... to come ...
