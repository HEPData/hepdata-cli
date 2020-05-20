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
$ hepdata [--verbose] find [TEXT] [-kw, --keyword TEXT]
$ hepdata [--verbose] download [TEXT] [--csv] [--root] [--yaml] [--yoda]
```

The option ```[--verbose]``` prints the hepdata url of the given search.

The argument ```[-kw, --keyword TEXT]``` defaults to "All", which returns the full metadata dictionary of the matches. Otherwise, it is used to filter the dictionary for specific keywords. An exact match of the keyword is first attempted, otherwise partial matches are accepted.

The options  ```[--csv] [--root] [--yaml] [--yoda]``` specify the download type. In all cases the files are contained in a .tar.gz archive.

## Examples

### Example 1:

```code
$ hepdata --verbose find 'reactions:"P P--> LQ LQ X"'
```
matches a single entry and returns full metadata dictionary.

### Example 2:

```code
$ hepdata --verbose find 'reactions:"P P--> LQ LQ"' --keyword=arxiv
```
matches a four entries and returns arXiv IDs (when available).

### Example 3:

```code
$ hepdata --verbose download 'reactions:"P P--> LQ LQ"' --csv
```
matches a four entries and downloads four csv.tar.gz archives.