# HEPData-CLI

## About

HEPData command-line interface to allow users to search, download, and upload to HEPData.

## Installation (temporary)

```code
$ git clone git@github.com:HEPData/hepdata-cli.git
$ pip install -e -user ~/path/to/hepdata-cli
```

## Usage

```code
$ hepdata-cli [-v/--verbose] find [TEXT] [-kw/--keyword TEXT] [-i/--ids IDTYPE]
$ hepdata-cli [-v/--verbose] download [IDS] [-f/--file-format FORMAT] [-i/--ids IDTYPE] [-t/--table TABLE-NUMBER]
```

The argument ```[-kw/--keyword TEXT]``` filters the search result dictionary for specific keywords.
An exact match of the keyword is first attempted, otherwise partial matches are accepted.

The argument ```[-i/--ids IDTYPE]``` accepts ```IDTYPE``` equal to ```arxiv```, ```hepdata``` or```inspire```.

The argument  ```[-f/--file-format FORMAT]``` accepts ```FORMAT``` equal to ```csv```, ```root```, ```yaml```, ```yoda```, or ```json```.
In the first four cases a .tar.gz archive is downloaded, in the last case a .json file is downloaded.

The argument  ```[-t/--table TABLE-NUMBER]``` accepts a number as input.
In this case only the speficied table is download as a .csv, .root, .yaml or .yoda file.

The ```hepdata-cli download``` and ```hepdata-cli find``` commands can be concatenated, if a ```IDTYPE``` is speficied for ```find```.
It is also possible to concatenate ```arxiv download```, form [pypi/arxiv-cli](https://pypi.org/project/arxiv-cli/), with ```hepdata-cli find```, if ```arxiv``` is used as ```IDTYPE```.

## Examples

### Example 1:

```code
$ hepdata-cli -v find 'reactions:"P P--> LQ LQ X"'
```
matches a single entry and returns full metadata dictionary.

### Example 2:

```code
$ hepdata-cli -v find 'reactions:"P P--> LQ LQ"' -kw year
```
matches a four entries and returns their publication years, as a dictionary.

### Example 3:

```code
$ hepdata-cli -v find 'reactions:"P P--> LQ LQ"' -i hepdata
```
matches a four entries and returns their hepdata ids, as a plain list.

### Example 4:

```code
$ hepdata-cli -v download $(hepdata-cli find 'reactions:"P P--> LQ LQ"' -i inspire) -i inspire -f csv
```
downloads four csv.tar.gz archives.

### Example 5:

```code
$ arxiv download $(hepdata-cli find 'reactions:"P P--> LQ LQ"' -i arxiv)
```
downloads two pdfs from the arXiv.