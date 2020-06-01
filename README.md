[![Travis Status](https://www.travis-ci.org/HEPData/hepdata-cli.svg?branch=master)](https://www.travis-ci.org/HEPData/hepdata-cli)
[![Coveralls Status](https://coveralls.io/repos/github/HEPData/hepdata-cli/badge.svg?branch=master)](https://coveralls.io/github/HEPData/hepdata-cli?branch=master)
[![License](https://img.shields.io/github/license/HEPData/hepdata-cli.svg)](https://github.com/HEPData/hepdata-cli/blob/master/LICENSE.txt)
[![GitHub Releases](https://img.shields.io/github/release/hepdata/hepdata-cli.svg?maxAge=2592000)](https://github.com/HEPData/hepdata-cli/releases)
[![PyPI Version](https://img.shields.io/pypi/v/hepdata-cli)](https://pypi.org/project/hepdata-cli/)
[![GitHub Issues](https://img.shields.io/github/issues/hepdata/hepdata-cli.svg?maxAge=2592000)](https://github.com/HEPData/hepdata-cli/issues)


# HEPData-CLI

## About

Command line interface (CLI) and application program interface (API) to allow users to search and download from HEPData.

The code is compatible with both Python 2 and Python 3.

## Installation (for users)

Install from [PyPI](https://pypi.org/) (coming soon):

```code
$ pip install --user hepdata-cli
$ hepdata-cli --help
```

## Installation (for developers)

Install from GitHub in a [virtual environment](https://docs.python.org/3/tutorial/venv.html):

```code
$ git clone https://github.com/HEPData/hepdata-cli.git
$ cd hepdata-cli
$ python3 -m venv ~/venv/hepdata-cli
$ source ~/venv/hepdata-cli/bin/activate
(hepdata-cli) $ pip install -e .[tests]
(hepdata-cli) $ hepdata-cli --help
(hepdata-cli) $ pytest --cov=hepdata_cli
```

## Usage

You can use HEPData-CLI both as a command-line interface (CLI) to search and download records from the HEPData database, or as a Python library to perform the same operations via its application program interface (API).


# CLI

```code
$ hepdata-cli [-v/--version, --help]
$ hepdata-cli [--verbose] find [TEXT] [-kw/--keyword TEXT] [-i/--ids IDTYPE]
$ hepdata-cli [--verbose] download [IDS] [-f/--file-format FORMAT] [-i/--ids IDTYPE] [-t/--table-name TABLE-NAME]
$ hepdata-cli [--verbose] fetch-names [IDS] [-i/--ids IDTYPE]
```

The command ```find``` searches the [HEPData](https://www.hepdata.net/) database for matches of ```TEXT```. The advanced search syntax from the website can be used.

The command ```download``` downloads records from the database (see options below).

The command ```fetch-names``` returns the names of the data tables in the records whose ids are supplied.

The argument ```[-kw/--keyword TEXT]``` filters the search result dictionary for specific keywords.
An exact match of the keyword is first attempted, otherwise partial matches are accepted.

The argument ```[-i/--ids IDTYPE]``` accepts ```IDTYPE``` equal to ```arxiv```, ```hepdata``` or```inspire```.

The argument  ```[-f/--file-format FORMAT]``` accepts ```FORMAT``` equal to ```csv```, ```root```, ```yaml```, ```yoda```, or ```json```.
In the first four cases a .tar.gz archive is downloaded, in the last case a .json file is downloaded.

The argument  ```[-t/--table TABLE-NUMBER]``` accepts a number as input.
In this case only the specified table is download as a .csv, .root, .yaml or .yoda file.

The ```hepdata-cli download/fetch-names``` and ```hepdata-cli find``` commands can be concatenated, if a ```IDTYPE``` is specified for ```find```.
It is also possible to concatenate ```arxiv download```, form [pypi/arxiv-cli](https://pypi.org/project/arxiv-cli/), with ```hepdata-cli find```, if ```arxiv``` is used as ```IDTYPE```.

# API

Equivalently to the above, these commands can be invoked by the API (in fact, the CLI is just a wrapper around the API).

```python
from hepdata_cli.api import Client
client = Client(verbose=False)
client.find(query, keyword, ids)
client.download(id_list, file_format, ids, table_name, download_dir)
client.fetch_names(id_list, ids)

```

## Examples

### Example 1 - a plain search:

```code
$ hepdata-cli -v find 'reactions:"P P--> LQ LQ X"'
```

or equivalently

```python
client.find('reactions:"P P--> LQ LQ X"')
```

matches a single entry and returns full metadata dictionary.

### Example 2 - search with keyword:

```code
$ hepdata-cli -v find 'reactions:"P P--> LQ LQ"' -kw year
```

or equivalently

```python
client.find('reactions:"P P--> LQ LQ"', keyword='year')
```

matches four entries and returns their publication years, as a dictionary.

### Example 3 - search for ids of records:

```code
$ hepdata-cli -v find 'reactions:"P P--> LQ LQ"' -i hepdata
```

or equivalently

```python
client.find('reactions:"P P--> LQ LQ"', ids='hepdata')
```

matches four entries and returns their hepdata ids, as a plain list.

### Example 4 - concatenate search with download using inspire ids:

```code
$ hepdata-cli -v download $(hepdata-cli find 'reactions:"P P--> LQ LQ"' -i inspire) -i inspire -f csv
```

or equivalently

```python
id_list = client.find('reactions:"P P--> LQ LQ"', ids='inspire')
client.download(id_list, ids='inspire', file_format='csv')
```

downloads four csv.tar.gz archives.

### Example 5 - concatenate search with download from arxiv-cli:

This example requires [arxiv-cli](https://github.com/jacquerie/arxiv-cli) to be installed, which is easily done via:

```code
$ pip install --user arxiv-cli
```

Then,

```code
$ arxiv download $(hepdata-cli find 'reactions:"P P--> LQ LQ"' -i arxiv)
```
or equivalently

```python
import arxiv_cli
import hepdata_cli
arxiv_client = arxiv_cli.Client()
hepdata_client = hepdata_cli.Client()
id_list = hepdata_client.find('reactions:"P P--> LQ LQ"', ids='arxiv')
arxiv_client.download(id_list)
```

downloads two pdfs from the arXiv.

### Example 6 - find table names in records:

```code
$ hepdata-cli fetch-names $(hepdata-cli find 'reactions:"P P--> LQ LQ"' -i hepdata) -i hepdata
```

or equivalently

```python
id_list = client.find('reactions:"P P--> LQ LQ"', ids='hepdata')
client.fetch_names(id_list, ids='hepdata')
```

returns all table names in the four matching records.