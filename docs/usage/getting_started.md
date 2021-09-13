# Getting started

This guide walks through some of the important (and some of the lesser important) features of *kiara*, the goal is to introduce
new users to the overall framework, so they can get a feeling for what it can do, and whether it might be useful for their
own usage scenarios.

As example data, we'll be using two csv files that were created by my colleague [Lena Jaskov](https://github.com/yaslena): [files](https://github.com/DHARPA-Project/kiara_modules.playground/tree/develop/examples/data/journals)

The files contain information about connection (edges) between medical journals (``JournalEdges1902.csv``), as well as additional metadata for the journals themselves (``JournalNodes1902.csv``). We'll use that data to create table and graph structures with *kiara*.

## Setting up kiara

For now, there are no published binary versions of kiara, so we'll install the Python package in a virtual environment.
While we're at it we'll check out the [kiara_modules.playgrounds repository](https://github.com/DHARPA-Project/kiara_modules.playground), because we can use that later to create our own *kiara* modules and pipelines:

### On Linux & Mac OS X (using `make`)

```console
git clone https://github.com/DHARPA-Project/kiara_modules.playground.git
cd kiara_modules.playground
python3 -m venv .venv
source .venv/bin/activate
make init
```

This will take a while, because it sets up a full-blown development environment. Which is not really necessary for us
at this stage, but hey...

### Windows (or manual pip install)

It's impossible to describe all the ways Python can be installed on a machine, and virtual- (or conda-)envs can be created, so I'll assume you know how to do this.

One simple way is to install the [Anaconda (individual edition)](https://docs.anaconda.com/anaconda/install/index.html), then use the Anaconda navigator to create a new environment, install the 'git' package in it (if your system does not already have it), and use the 'Open Terminal' option of that environment to start up a terminal that has that virtual-/conda-environment already activated.

Once that is done, create and change into a directory where you want this project folder to live, make sure your virtual- or conda-env is activated (if you used the Anaconda navigator to open the Terminal, it should be, otherwise you could use something like `pip -V` and look at the output path), then do:

!!! note
    If you are using Windows, there might be a problem installing one of the dependencies *`python-levenshtein`) because it requires a C++ compiler installed. If you are using conda, any potential problems can be avoided by installing the `python-levenshtein` conda package before 'pip install'-ing the local git repo.
    Let me know if this is causing problems in your environment, and I'll try to find a better way to deal with this.

```console
# ensure activated virtual- or conda environment
git clone https://github.com/DHARPA-Project/kiara_modules.playground.git
cd kiara_modules.playground
# the next command is optional, ignore if not using conda
conda install -c conda-forge python-levenshtein
pip install --extra-index-url https://pypi.fury.io/dharpa/ -U -e .[all_dev]
```


## Checking for available operations

First, let's have a look which operations are available, and what we can do with them:

{{ cli("kiara", "operation", "list", max_height=320) }}

!!! note
    In this guide we'll use the term *operation* to indicate an entity that transforms data in some way or form. *kiara*
    also has the concept of *module* (the differences are explained in more detail [here](../concepts/index.md)), and in most
    cases the meaning of '*module*' and '*operation*' is roughly the same. Especially in the context of this 'Getting started'
    guide. Nonetheless, keep in mind that technically both terms refer to different things.

## Importing data, and creating a table

Tables are arguably the most used (and useful) data structures in data science and data engineering. They come in different
forms; some people call them spreadsheets, or dataframes. We're not that fancy, so we won't do that: we'll call them tables.
Also, when we talk about tables in *kiara*-land, we specifically talk about [Apache Arrow Tables](https://arrow.apache.org/docs/cpp/tables.html#tables),
because *kiara* really likes the [Apache Arrow project](https://arrow.apache.org/docs/index.html); there is a high probability that it will become a de-facto standard in this space (if it isn't already). Why Arrow tables are better than others is a topic for another time, plus, in practical terms the underlying implementation of the data structures that are used by *kiara* won't matter that much to most users anyway.

A depressingly large amount of data comes in csv files, which is why we'll use one as an example here. Specifically, we will
use [``JournalNodes1902.csv``](https://github.com/DHARPA-Project/kiara_modules.playground/blob/develop/examples/data/journals/JournalNodes1902.csv). This file contains information about historical medical
journals (name, type, where it was from, etc.). We want to convert this file into a 'proper' table structure, because
that will make subsequent processing faster, and also simpler in a lot of cases.

### Finding the right command, and how to use it

The best practice on how to 'onboard' any type of external data is not yet established, but one way that will always be supported
is to 'import' the file containing the data first, then convert it to the target 'internal' *kiara* data type. So let's do that here...

#### Importing the 'raw' file

After looking at the ``kiara operation list`` output, it looks like the ``file.import_from.local.file_path`` module might be just what we need. *kiara* has the [``run``](../running_operations) sub-command, which is used to execute operations. If we
only provide a module name, and not any input, this command will tell us what it expects:

{{ cli("kiara", "run", "file.import_from.local.file_path", extra_env={"KIARA_DATA_STORE": "/tmp/kiara/getting_started"}) }}

!!! note
    The output of this command may show two other inputs (apart from `source`): `save` and `aliases`. There is a good chance that
    those two will be gone in the future, so just pretend you didn't see them, otherwise what follows might or might not appear a bit silly.

As makes obvious sense, we need to provide a ``source`` input, of type ``file_path`` (basically, a string). The *kiara* commandline interface can
take complex inputs like dicts, but fortunately this is not necessary here. If you ever come into a situation where you need that, check out [this section](../..//usage/#complex-inputs).

For simple inputs like string-type things, all we need to do is provide the input name, followed by '=' and the value itself:

{{ cli("kiara", "run", "file.import_from.local.file_path", "source=examples/data/journals/JournalNodes1902.csv", max_height=340, extra_env={"KIARA_DATA_STORE": "/tmp/kiara/getting_started"}) }}

As you can see from the terminal output, this produced one piece of output data: `value_item` (referring to the imported file), and it displays a some metadata of the file in question for us. By itself, this doesn't do anything yet, it just reads the file and then stops. What we want in this case is to 'save' the file, so we can refer to it again later. The process of 'saving' a value in *kiara* persists it into the *kiara* data store, gives it an internal unique id (string), and allows the user to 'tag' the value with one or multiple aliases. Aliases are names that are meaningful to the user, as to make it easy to find and identify an item later on.

*kiara* supports saving any of the output values of a `kiara run` command via the `--save` flag. This `--save` parameter takes a single string as argument, and can be used in two ways:

- if you want to save all output fields of a `run` you can just provide a single string (for example `imported_journal_csv`) as the parameter. In this case, *kiara* will store all result items with an auto-generated alias in the form of `[save_argument]__[field_name]`. In our case this would result in one item being store in the data store, with the alias `imported_journal_csv__value_item`.
- if you want to save only a subset of result values, or want to have more control about the aliases those results get, you can use the `--save` parameter for every field you want to persist. In this case the argument to `--save` must be in the form of: `[field_name]=[alias]`. You can use the parameter multiple times, with different field names.

In our case, lets opt for the second option:

{{ cli("kiara", "run", "--save", "value_item=my_first_file", "file.import_from.local.file_path", "source=examples/data/journals/JournalNodes1902.csv", max_height=340, extra_env={"KIARA_DATA_STORE": "/tmp/kiara/getting_started"}) }}

#### Checking the data store

To check whether that worked, we can list all of our items in the data store, and see if the one we just created is in there:

{{ cli("kiara", "data", "list", cache_key="1st_run_data_list", extra_env={"KIARA_DATA_STORE": "/tmp/kiara/getting_started"}) }}

All right! Looks like this worked.

#### Converting an imported csv file into a table

Csv files are usually not much use by themselves, they need to be converted into a table-structure so we can efficiently query then.
This usually also makes sure that the structure and format of the file is valid.

Let's ask kiara what 'table' related operations it has available:

{{ cli("kiara", "operation", "list", "table") }}

!!! note
    If you add strings to the end of any `list` command in *kiara*, they act as filters.

Righto, looks like `file.convert_to.table` might be our ticket! Let's see what it does:

{{ cli("kiara", "operation", "explain", "file.convert_to.table") }}

So, it needs an input `value_item` of type `file` as input, and will return a same-named output of type `table`. Looks good. Here is how we run this:

{{ cli("kiara", "run", "file.convert_to.table", "value_item=value:my_first_file", extra_env={"KIARA_DATA_STORE": "/tmp/kiara/getting_started"}) }}

!!! note
    In this example we pre-pend the right side of the `value_item=` argument with `value:`. This is necessary to make it clear to *kiara* that we mean
    a dataset that lives in its data store. Otherwise, *kiara* would have just interpreted the input as a string, and since that is of the wrong input type
    (we needed a table), it would have thrown an error.

That output looks good, right? Much more table-y then before. Only thing is: we want to again 'save' this output, so we can use it later directly. No big deal, just like last time:

{{ cli("kiara", "run", "--save", "value_item=my_first_table", "file.convert_to.table", "value_item=value:my_first_file", extra_env={"KIARA_DATA_STORE": "/tmp/kiara/getting_started"}) }}

#### Checking the data store, again

Now, let's look again at the content of the *kiara* data store:

{{ cli("kiara", "data", "list", cache_key="2nd_run_data_list", extra_env={"KIARA_DATA_STORE": "/tmp/kiara/getting_started"}) }}

As you can see, there are 2 items now: one `file`, and one `table`. If you ever want to get more details about any of the items in the data store, you can use one of those commands:

##### `kiara data explain`

{{ cli("kiara", "data", "explain", "my_first_table") }}

This command prints out the metadata *kiara* has stored about a value item.

One thing that is noteworthy here is the ``load_config`` section in the metadata. When saving the value, *kiara* automatically
generated this configuration, and it can be used later to load and use the exact same table file, in another workflow.

##### `kiara data load`

{{ cli("kiara", "data", "load", "my_first_table") }}

This command loads the actual data, and prints out its content (or a representation of it that makes sense in a terminal-context).

One thing that is noteworthy here is the ``load_config`` section in the metadata. When saving the value, *kiara* automatically
generated this configuration, and it can be used later to load and use the exact same table file, in another workflow.

## Querying the table data

This section is a bit more advanced, so you can skip it if you want. It's just to show an example of what can be done with
a stored table data item.

We'll be using the [sql](https://en.wikipedia.org/wiki/SQL) query language to find the names and types of all journals from Berlin. The query for this is:

```sql
select Label, JournalType from data where City='Berlin'
```

The *kiara* module we are going to use is called ``table.query.sql``. Let's check again the parameters this module expects:

{{ cli("kiara", "run", "table.query.sql", extra_env={"KIARA_DATA_STORE": "/tmp/kiara/getting_started"}) }}

Aha. ``table``, and ``query`` are required. Good, we have both. In this example we'll use the data item we've stored as input for another workflow. That goes like this:

{{ cli("kiara", "run", "table.query.sql", "table=value:my_first_table", "query=\"select Label, JournalType from data where City=\'Berlin\'\"", extra_env={"KIARA_DATA_STORE": "/tmp/kiara/getting_started"}, max_height=240) }}

Note how we use the ``value:``-prefix here, to signify to *kiara* that what follows is indeed a reference to a dataset, and not a string...

### Saving the result of the query

As it is, the result of this query won't be saved anywhere. This might be fine for queries in exploratory-type situations. But in some cases
we might want to store the result of our work, similar to how we imported the original table in the first place. The ``kiara run`` command can do that, using the ``--save`` flag. It takes as argument a string. If that string contains a '=', it is interpreted as a key value pair where the key is the name of the field we want to save, and the value the alias we want to save it under. Here is how that goes:

{{ cli("kiara", "run", "table.query.sql", "--output=silent", "--save", "query_result=berlin_journals", "table=value:my_first_table", "query=\"select Label, JournalType from data where City=\'Berlin\'\"", extra_env={"KIARA_DATA_STORE": "/tmp/kiara/getting_started"}, max_height=240) }}

Here we've also used the ``--output=silent`` option, since we've seen that result before.

From looking at the output, it seems that saving our result has worked. We can make sure by letting *kiara* 'explain' to us the data that is stored under the alias 'berlin_journals':

{{ cli("kiara", "data", "explain", "berlin_journals", extra_env={"KIARA_DATA_STORE": "/tmp/kiara/getting_started"}, max_height=240) }}
