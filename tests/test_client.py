# -*- coding: utf-8 -*-

import pytest
import os
import sys

from click.testing import CliRunner

from hepdata_cli.api import Client, mkdir
from hepdata_cli.cli import cli


# arguments for testing

test_find_arguments = [
    ('reactions:"P P--> LQ LQ X"', None, None),
    ('reactions:"P P--> LQ LQ"', 'year', None),
    ('reactions:"P P--> LQ LQ"', 'arxiv', None),
    ('reactions:"P P--> LQ LQ"', None, 'arxiv'),
    ('reactions:"P P--> LQ LQ"', None, 'hepdata'),
]

test_download_arguments = [
    (["73322"], "json", "hepdata", ''),
    (["1222326", "1694381", "1462258", "1309874"], "csv", "inspire", ''),
    (["61434"], "yaml", "hepdata", "Table1"),
    (["1762350"], "yoda", "inspire", "Number density and Sum p_T pT>0.15 GeV/c"),
]

test_fetch_names_arguments = [
    (["73322"], "hepdata"),
    (["1222326", "1694381", "1462258", "1309874"], "inspire"),
]


# api testing

@pytest.mark.parametrize("query, keyword, ids", test_find_arguments)
def test_api_find(query, keyword, ids):
    client = Client(verbose=True)
    search_result = client.find(query, keyword, ids)
    if ids is None:
        assert type(search_result) is list
        if len(search_result) > 0:
            assert all([type(entry) is dict for entry in search_result])
    else:
        assert type(search_result) is str


@pytest.mark.parametrize("id_list, file_format, ids, table", test_download_arguments)
def test_api_download(id_list, file_format, ids, table):
    test_download_dir = './.pytest_downloads/'
    mkdir(test_download_dir)
    assert len(os.listdir(test_download_dir)) == 0
    client = Client(verbose=True)
    client.download(id_list, file_format, ids, table, test_download_dir)
    assert len(os.listdir(test_download_dir)) > 0
    for entry in os.listdir(test_download_dir):
        os.remove(test_download_dir + "/" + entry)
    assert len(os.listdir(test_download_dir)) == 0
    os.rmdir(test_download_dir)


@pytest.mark.parametrize("id_list, ids", test_fetch_names_arguments)
def test_api_fetch_names(id_list, ids):
    client = Client(verbose=True)
    lnames = client.fetch_names(id_list, ids)
    assert(type(lnames) is list)
    if len(lnames) > 0:
        assert(all(type(names) is list for names in lnames))


# cli testing

@pytest.mark.parametrize("query, keyword, ids", test_find_arguments)
def test_cli_find(query, keyword, ids):
    runner = CliRunner()
    result = runner.invoke(cli, ['find', query, '-kw', keyword, '-i', ids])
    assert result.exit_code == 0


@pytest.mark.parametrize("id_list, file_format, ids, table", test_download_arguments)
def test_cli_download(id_list, file_format, ids, table):
    runner = CliRunner()
    result = runner.invoke(cli, ['download'] + id_list + ['-f', file_format, '-i', ids, '-t', table])
    assert result.exit_code == 0


@pytest.mark.parametrize("id_list, ids", test_fetch_names_arguments)
def test_cli_fetch_names(id_list, ids):
    runner = CliRunner()
    if sys.version_info.major == 2:
        result = runner.invoke(cli, ['fetch_names'] + id_list + ['-i', ids])
    elif sys.version_info.major == 3:
        result = runner.invoke(cli, ['fetch-names'] + id_list + ['-i', ids])
    assert result.exit_code == 0
