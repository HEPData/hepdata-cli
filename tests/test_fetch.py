# -*- coding: utf-8 -*-

import pytest
import sys

from click.testing import CliRunner

from hepdata_cli.api import Client
from hepdata_cli.cli import cli


# arguments for testing

test_fetch_names_arguments = [
    (["73322"], "hepdata"),
    (["1222326", "1694381", "1462258", "1309874"], "inspire"),
]


# api testing

@pytest.mark.parametrize("id_list, ids", test_fetch_names_arguments)
def test_api_fetch_names(id_list, ids):
    client = Client(verbose=True)
    lnames = client.fetch_names(id_list, ids)
    assert(type(lnames) is list)
    if len(lnames) > 0:
        assert(all(type(names) is list for names in lnames))


# cli testing

@pytest.mark.parametrize("id_list, ids", test_fetch_names_arguments)
def test_cli_fetch_names(id_list, ids):
    runner = CliRunner()
    if sys.version_info.major == 2:
        result = runner.invoke(cli, ['fetch_names'] + id_list + ['-i', ids])
    elif sys.version_info.major == 3:
        result = runner.invoke(cli, ['fetch-names'] + id_list + ['-i', ids])
    assert result.exit_code == 0
