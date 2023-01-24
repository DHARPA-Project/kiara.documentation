[![PyPI status](https://img.shields.io/pypi/status/kiara.documentation.svg)](https://pypi.python.org/pypi/kiara.documentation/)
[![PyPI version](https://img.shields.io/pypi/v/kiara.documentation.svg)](https://pypi.python.org/pypi/kiara.documentation/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/kiara.documentation.svg)](https://pypi.python.org/pypi/kiara.documentation/)
[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2FDHARPA-Project%2Fkiara%2Fbadge%3Fref%3Ddevelop&style=flat)](https://actions-badge.atrox.dev/DHARPA-Project/kiara.documentation/goto?ref=develop)
[![Coverage Status](https://coveralls.io/repos/github/DHARPA-Project/kiara.documentation/badge.svg?branch=develop)](https://coveralls.io/github/DHARPA-Project/kiara.documentation?branch=develop)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# [**kiara**](https://dharpa.org/kiara.documentation) plugin: (documentation)

Kiara user documentation.

 - Documentation: [https://DHARPA-Project.github.io/kiara.documentation](https://DHARPA-Project.github.io/kiara.documentation)
 - Code: [https://github.com/DHARPA-Project/kiara.documentation](https://github.com/DHARPA-Project/kiara.documentation)


## Description

TODO

## Development

### Requirements

- Python (version >= 3.8)
- conda
- git


### Prepare development environment

### Using conda (recommended)

```
conda create -n kiara_documentation python=3.9
conda activate kiara_documentation
```

### Using venv

```
python -m venv .venv
.venv/bin/activate
```

## Check out the source code

First, fork the [kiara.documentation](https://github.com/DHARPA-Project/kiara.documentation) repository into your personal Github account.

Then, use the resulting url (in my case: https://github.com/makkus/kiara.documentation.git) to clone the repository locally:

```
git clone https://github.com/<YOUR_FORKED_GITHUB_ID>/kiara.documentation
```

## Install the kiara documentation package into it

```
cd kiara.documentation
pip install -e '.[dev_utils]'
```

## Install asciinet dependency (optional)

```
pip install 'git+https://github.com/cosminbasca/asciinet.git#egg=asciinet&subdirectory=pyasciinet'
```

This is not strictly necessary, documentation generation won't fail without it, but any ascii-graphs won't be generated. This also needs Java to be available on your machine.

## Try it out

If you followed the instructions above, you should see an additional `doc` subcommand when doing a `kiara --help`. Check out the available commands by using the `--help` flag.

The main command to use is `serve`, which builds and serves the current documenation website:

```console
kiara doc serve
...
...
```

This will create the documentation, and run a webserver on [http://localhost:8000](http://localhost:8000) where you can preview the generated documentation site.
The first startup will take a bit, because some of the pages use dynamically generated results to prevent the documentation becoming
out-of-date easily (and as a test against regressions). Those results are cached though, so the 2nd time around startup should be quicker.

The 'serve' command will watch documents under `docs`, if any of them is changed, it will auto-create the changed documentation page,
and reload the browser(s) that are viewing it.

Another important command is `cache clear`, which cleares the build cache of the dynamic commands that were executed while building the page for the first time.

## Copyright & license

This project is MPL v2.0 licensed, for the license text please check the [LICENSE](/LICENSE) file in this repository.
