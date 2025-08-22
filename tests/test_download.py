# -*- coding: utf-8 -*-

import pytest
import os
import shutil

from click.testing import CliRunner

from hepdata_cli.api import Client, mkdir
from hepdata_cli.cli import cli


# initial clean up

def cleanup(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    assert len(os.listdir(directory)) == 0
    os.rmdir(directory)


test_download_dir = './.pytest_downloads/'
mkdir(test_download_dir)  # in case it is not there
cleanup(test_download_dir)


# arguments for testing

test_api_download_arguments = [
    (["73322"], "json", "hepdata", ''),
    (["1222326", "1694381", "1462258", "1309874"], "csv", "inspire", ''),
    (["61434"], "yaml", "hepdata", "Table1"),
    (["1762350"], "yoda", "inspire", "Number density and Sum p_T pT>0.15 GeV/c"),
    (["2862529"], "yoda.h5", "inspire", "95% CL upper limit on XSEC times BF"),
    (["2862529"], "yoda.h5", "inspire", '')
]

test_cli_download_arguments = [
    (["2862529"], "json", "inspire", ''),
    (["1222326", "1694381", "1462258", "1309874"], "root", "inspire", ''),
    (["61434"], "yaml", "hepdata", "Table2"),
]


# api testing

@pytest.mark.parametrize("id_list, file_format, ids, table", test_api_download_arguments)
def test_api_download(id_list, file_format, ids, table):
    test_download_dir = './.pytest_downloads/'
    mkdir(test_download_dir)
    assert len(os.listdir(test_download_dir)) == 0
    client = Client(verbose=True)
    client.download(id_list, file_format, ids, table, test_download_dir)
    assert len(os.listdir(test_download_dir)) > 0
    cleanup(test_download_dir)


# cli testing

@pytest.mark.parametrize("id_list, file_format, ids, table", test_cli_download_arguments)
def test_cli_download(id_list, file_format, ids, table):
    test_download_dir = './.pytest_downloads/'
    mkdir(test_download_dir)
    assert len(os.listdir(test_download_dir)) == 0
    runner = CliRunner()
    result = runner.invoke(cli, ['download'] + id_list + ['-f', file_format, '-i', ids, '-t', table, '-d', test_download_dir])
    assert result.exit_code == 0
    assert len(os.listdir(test_download_dir)) > 0
    cleanup(test_download_dir)
