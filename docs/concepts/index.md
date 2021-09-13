# Overview

This section explains some of the concepts and terminology used in *kiara*. Unfortunately, there are some terms that *almost* mean the same
thing, and unless you are developing on the *kiara* core the distinctions are not relevant. But since some of us are developing on the *kiara* core,
it's important to be able to express the exact thing we are talking about. This is the main reason why this part of the documentation exists: to have a place
to list the exact meanings of the words that are used across *kiara*-land.

## Modules, pipelines, and operations

The main confusion when talking about *kiara*s internals revolves around the concept of 'modules'. It's often used as a blanket-term
to refer to an executable unit within *kiara* (esp. when talking about the general concept of 'modularity'), which I think in the
interest of brevity is a valid thing to do.

### Modules

Modules are the building blocks of *kiara*. The central element of a *kiara* module is a [pure](https://en.wikipedia.org/wiki/Pure_function) function which performs a defined piece of work. A module also contains a type information/schema of the input values the function takes, as well as of the output it produces.

In the interest of efficiency, and to not have to repeat code across different modules overly much, *kiara* modules can be configured, and depending on the configuration the inputs- and output schemas can change, as so can the processing function within the module. A configured *module* is refered to as *module instance*, or *operation*.

In most cases *kiara* modules are implemented as Python classes, inheriting from the [KiaraModule](https://dharpa.org/kiara/api_reference/kiara.module/#kiara.module.KiaraModule) abstract base class.

An easy way to find all available modules is the ``kiara module list`` command. For details about a specific module type, ``kiara module explain ...`` is a good choice:

{{ cli("kiara", "module", "explain", "value.hash", max_height=240) }}

### Pipelines

Im some cases such simple *kiara* modules are enough to do meaningful pieces of work. In other cases, we want to assemble two or more of those core modules, because otherwise we'd have to write a new Python module that incorporates the functionality of smaller-scoped modules that already exist. The result of assembling some modules
is called a *pipeline*. The connecting is done by defining which inputs of which internal modules are connected to which outputs of other internal modules. There will be some inputs left over, not connected. Those become the inputs of the *pipeline* itself. The outputs of a *pipeline* are all or a subset of each individual, contained module.
You may have noticed that after assembling a pipeline in this way, we end up with an entity that performs a defined piece of work, and contains type information/schema of the input values it takes, as well as the output it produces. This means, a *pipeline* itself can also be considered a *module*, and itself can be part of another *pipeline*, and so on.

*kiara* provides a few helpful commands under the ``kiara pipeline`` subcommands. One of them is ``kiara pipeline explain``:

{{ cli("kiara", "pipeline", "explain", "logic.xor", max_height=320) }}

### Operations

Operations are what users usually interact with. They have a fixed id (``kiara operation list``), a fixed set of well-defined inputs and outputs, and a well-defined, (usually) [idempotent](https://en.wikipedia.org/wiki/Idempotence) way of transforming inputs into outputs. Operations are defined uniquely by their module type and module configuration (which means, the same module type configured in the same way always results in the same operation). You can find out those details using the *kiara* command-line interface:

{{ cli("kiara", "operation", "explain", "file.calculate_hash.sha3_256", max_height=240) }}

Some modules don't require any configuration (either because they can't be configured, or have default values for all configuration options). If that is the case, *kiara* considers those also as operations, and includes the module type id in the list of operations automatically.

Every (top-level) pipeline a user interacts with can also act as an *operation*, in the same way a configured *module* can (since, as we've established earlier, every pipeline is also a module):

{{ cli("kiara", "operation", "explain", "logic.xor", max_height=240) }}


### More details

Yes, I know... this is more confusing than it seems like it should be... If you have a better idea how to name those things and concepts, I'd be more than happy to hear suggestions!

The following links go into more detail on each of the concepts:

  - [Modules](modules.md): the core building blocks of *kiara*
  - [Pipelines](pipelines.md): assembled *modules*
  - [Operations](operations.md): instantiated *modules* or *pipelines*
