[![PyPI status](https://img.shields.io/pypi/status/kiara_documentation.svg)](https://pypi.python.org/pypi/kiara/)
[![PyPI version](https://img.shields.io/pypi/v/kiara_documentation.svg)](https://pypi.python.org/pypi/kiara/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/kiara_documentation.svg)](https://pypi.python.org/pypi/kiara/)
[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2FDHARPA-Project%2Fkiara%2Fbadge%3Fref%3Ddevelop&style=flat)](https://actions-badge.atrox.dev/DHARPA-Project/kiara_documentation/goto?ref=develop)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# *kiara* usage documentation

The repository to hold the *kiara* user documentation sources.

 - Documentation: [https://dharpa.org/kiara_documentation](https://dharpa.org/kiara_documentation)
 - Code: [https://github.com/DHARPA-Project/kiara_documentation](https://github.com/DHARPA-Project/kiara_documentation)

## Development

### Requirements

- Python (version >=3.6 -- some make targets only work for Python >=3.7 though)
- pip, virtualenv
- git
- make
- [direnv](https://direnv.net/) (optional)


### Prepare development environment

If you only want to work on the modules, and not the core *Kiara* codebase, follow the instructions below. Otherwise, please
check the notes on how to setup a *Kiara* development environment under (TODO).

```console
git clone https://github.com/DHARPA-Project/kiara_documentation.git
cd kiara_documentation
python3 -m venv .venv
source .venv/bin/activate
make init
```

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
cd path/to/kiara_documentation
source .venv/bin/activate
kiara --help  # or whatever, point is, kiara should be available again for you now
```

### ``make`` targets

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
