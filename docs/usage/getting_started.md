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


## Checking for available modules

First, let's have a look which modules are available, and what we can do with them:

{{ cli("kiara", "module", "list", max_height=320) }}

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

So, after looking at the ``kiara module list`` output, it looks like the ``table.import.from_local_file`` module might be a good fit for us. *kiara* has the [``run``](../running_modules) sub-command, which is used to execute modules. If we
only provide a module name, and not any input, this command will tell us what it expects:

{{ cli("kiara", "run", "table.import.from_local_file", extra_env={"KIARA_DATA_STORE": "/tmp/kiara/getting_started"}) }}

As makes obvious sense, we need to provide a ``path`` input, of type ``string``. The *kiara* commandline interface can
take complex inputs like dicts, but fortunately this is not necessary here. If you ever come into a situation where you need this, check out [this section](../..//usage/#complex-inputs).

For simple inputs like strings, all we need to do is provide the input name, followed by '=' and the value itself:

{{ cli("kiara", "run", "table.import.from_local_file", "path=examples/data/journals/JournalNodes1902.csv", max_height=340, extra_env={"KIARA_DATA_STORE": "/tmp/kiara/getting_started"}) }}

As you can see from the terminal output, this produced 2 pieces of output data: `table` and `value_id`. *kiara* tries to tell us what the values of each of the fields are, and prints a preview of them on the terminal.

### Checking the data store

To check whether that worked, we can list all of our items in the data store, and see if the one we just created is in there:

{{ cli("kiara", "data", "list", cache_key="1st_run_data_list", extra_env={"KIARA_DATA_STORE": "/tmp/kiara/getting_started"}) }}

Hm. No? What to do, what to do? Maybe the command we just ran can '--help' us?

{{ cli("kiara", "data", "list", "--help") }}

Right. Something about aliases... Let's see what happens if we use this ``--all`` thing...

{{ cli("kiara", "data", "list", "--all", cache_key="2nd_run_data_list", extra_env={"KIARA_DATA_STORE": "/tmp/kiara/getting_started"}) }}

All right! It seems there is something in there after all!

Here is what happened: we imported our table, but didn't specify the ``aliases`` input when running it. That means kiara didn't bother with aliases, and just imported our table without doing anything else, like assigning an alias. And the ``data list`` sub-command doesn't print any values that don't have
an alias, by default.

It did import our table though. It actually did more than that: it also imported the original csv file, along with the table that was generated from it. This is because *kiara* tries to keep an unbroken chain of record of every operation that is done with a dataset, in order to be able to later re-run and investigate a datasets history. Why this is use- (and power-)full is a discussion for another usage guide, but suffice to say: it is the reason why we see 2 items in our list.

### Importing data, with alias

So, let's try that again, this time with alias:

{{ cli("kiara", "run", "table.import.from_local_file", "path=examples/data/journals/JournalNodes1902.csv", "aliases=my_first_table", cache_key="2nd_run_table_import", max_height=200, extra_env={"KIARA_DATA_STORE": "/tmp/kiara/getting_started"}) }}

And, if everything went right, issuing ``data list --all`` command again should now be a bit more helpful:

{{ cli("kiara", "data", "list", "--all", cache_key="3rd_run_data_list", extra_env={"KIARA_DATA_STORE": "/tmp/kiara/getting_started"}) }}

One thing that is interesting: our 2-nd run didn't add a new data item for the table (with a new id), all it did was to add an alias for the existing one. This is because *kiara* is smart enough that it can, in some cases, see that two datasets are the same, and therefore it doesn't need to store the 2nd copy seperately. Which saves hard-disk space, among other things.

Another thing of note: *kiara* added an ``@1`` appendix to the alias we specified. This is the version of this alias within the *kiara* data store, and it is done automatically, so there is always a 'fixed' name you can use to refer to a dataset. If you would save a different table under the same alias, *kiara* would automatically increase the version number for the new dataset. You can always refer to a dataset using just the alias string; if you do that, *kiara* will pick the latest version that was stored under that alias.

Now that our table is safely imported, let's have a look at the metadata *kiara* has stored for this specific item (we could also use the id in the following command, by the way):

{{ cli("kiara", "data", "explain", "my_first_table", max_height=320, extra_env={"KIARA_DATA_STORE": "/tmp/kiara/getting_started"}) }}

This metadata is useful internally, because it enables *kiara* to be very selective about which parts of a dataset
it actually loads into memory, if any.

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

## Generating a network graph

Since what we actually want to do is generating a network graph from our two csv files, we'll have a look at the list of
modules again, and it looks like the ``network.graph.import.from_local_files`` one might do what we need.

But we are not sure. Luckily, *kiara* has some ways to give us more information about a module.

The first one is the ``module explain-type`` command:

{{ cli("kiara", "module", "explain-type", "network.graph.import.from_local_files", max_height=320, extra_env={"KIARA_DATA_STORE": "/tmp/kiara/getting_started"}) }}

Uh. That's a handful. To be honest, that's mostly useful for when you want to start creating modules or pipelines
for *kiara* yourself. The ``module explain-instance`` command is more helpful, though:

{{ cli("kiara", "module", "explain-instance", "network.graph.import.from_local_files", max_height=320, extra_env={"KIARA_DATA_STORE": "/tmp/kiara/getting_started"}) }}

The 'inputs' section is most interesting, it's basically the same information we get from running ``kiara run`` without any inputs. Using the information from that output, and after looking at the headers of our csv files, we can figure out how to assemble our command:

{{ cli("kiara", "run", "network.graph.import.from_local_files", "edges_path=examples/data/journals/JournalEdges1902.csv", "source_column=Source", "target_column=Target", "nodes_path=examples/data/journals/JournalNodes1902.csv", "nodes_table_index=Id", "--save", "graph=generate_graph_from_csvs.graph", extra_env={"KIARA_DATA_STORE": "/tmp/kiara/getting_started"}) }}

!!! note
    Yes, we could use the nodes table we loaded earlier here. But we don't. For reasons that have nothing to do with what makes sense here.

To confirm our graph is stored, let's check the data store:

{{ cli("kiara", "data", "explain", "generate_graph_from_csvs.graph", extra_env={"KIARA_DATA_STORE": "/tmp/kiara/getting_started"}) }}

## Investigating the graph

Now we might want to have a look at some of the intrinsic properties of our graph. For that, we will use the ``network.graph.properties`` module:

{{ cli("kiara", "run", "network.graph.properties", "graph=value:generate_graph_from_csvs.graph", "--save", "graph_properties_workflow", extra_env={"KIARA_DATA_STORE": "/tmp/kiara/getting_started"}) }}

## Finding the shortest path

Another thing we can do is finding the shortest path between two nodes:

{{ cli("kiara", "run", "network.graph.find_shortest_path", "graph=value:generate_graph_from_csvs.graph", "source_node=1", "target_node=2", extra_env={"KIARA_DATA_STORE": "/tmp/kiara/getting_started"}) }}

That's that, for now. This is just a first draft, let me know all the things I should change, explain better, etc.
