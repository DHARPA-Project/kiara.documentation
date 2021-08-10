[![PyPI status](https://img.shields.io/pypi/status/kiara.documentation.svg)](https://pypi.python.org/pypi/kiara/)
[![PyPI version](https://img.shields.io/pypi/v/kiara.documentation.svg)](https://pypi.python.org/pypi/kiara/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/kiara.documentation.svg)](https://pypi.python.org/pypi/kiara/)
[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2FDHARPA-Project%2Fkiara%2Fbadge%3Fref%3Ddevelop&style=flat)](https://actions-badge.atrox.dev/DHARPA-Project/kiara.documentation/goto?ref=develop)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# *kiara* usage documentation

The repository to hold the *kiara* user documentation sources.

 - Documentation: [https://dharpa.org/kiara.documentation](https://dharpa.org/kiara.documentation)
 - Code: [https://github.com/DHARPA-Project/kiara.documentation](https://github.com/DHARPA-Project/kiara.documentation)

## Development

### Requirements

- Python (version >=3.6 -- some make targets only work for Python >=3.7 though)
- pip, virtualenv
- git
- make (on Linux / Mac OS X -- optional)


### Prepare development environment

#### Linux & Mac OS X (using make)

For UNI*-like operating system, setting up a development environment is relatively easy:

```console
git clone https://github.com/DHARPA-Project/kiara.documentation.git
cd kiara.documentation
python3 -m venv .venv
source .venv/bin/activate
make init
```

#### Windows (or manual pip install)

It's impossible to lay out all the ways Python can be installed on a machine, and virtual- (or conda-)envs can be created, so I'll assume you know how to do this.
One simple way is to install the [Anaconda (individual edition)](https://docs.anaconda.com/anaconda/install/index.html), then use the Anaconda navigator to create a new environment, install the 'git' package in it (if your system does not already have it), and use the 'Open Terminal' option of that environment to start up a terminal that has that virtual-/conda-environment activated.

Once that is done, `cd` into a directory where you want this project folder to live, and do:

```console
# make sure your virtual env is activated!!!
git clone https://github.com/DHARPA-Project/kiara.documentation.git
cd kiara.documentation
pip install --extra-index-url https://pypi.fury.io/dharpa/ -U -e .[all_dev]
```

#### Try it out

After this is done, you should be able to run the included example module via:

```console
kiara run kiara_documentation.kiara_documentation.example text_1="xxx" text_2="yyy"
...
...
```

### Work on documentation

Once the development environment is set up, you can start the file watcher and doc auto-builder:

```
make serve-docs
```

Point your browser to: http://localhost:8000 and start editing markdown files. The rendered changes should appear more or less instantly (often less than more -- but it should be good enough) in your browser.

### Re-activate the development environment

The 'prepare' step from above only has to be done once. After that, to re-enable your virtual environment,
you'll need to navigate to the directory again (wherever that is, in your case), and run the ``source`` command from before again:

```console
cd path/to/kiara.documentation
source .venv/bin/activate  # if it isn't activated already, for example by the Anaconda navigator
kiara --help  # or whatever, point is, kiara should be available again for you now
```

### ``make`` targets (Linux & Mac OS X)

- ``init``: init development project (install project & dev dependencies into virtualenv, as well as pre-commit git hook)
- ``update-dependencies``: update development dependencies (mainly the core ``kiara`` package from git)
- ``flake``: run *flake8* tests
- ``mypy``: run mypy tests
- ``test``: run unit tests
- ``docs``: create static documentation pages (under ``build/site``)
- ``serve-docs``: serve documentation pages (incl. auto-reload) for getting direct feedback when working on documentation
- ``clean``: clean build directories

For details (and other, minor targets), check the ``Makefile``.


### Running tests

``` console
> make test
# or
> make coverage
```


## Copyright & license

This project is MPL v2.0 licensed, for the license text please check the [LICENSE](/LICENSE) file in this repository.

[Copyright (c) 2021 DHARPA project](https://dharpa.org)
