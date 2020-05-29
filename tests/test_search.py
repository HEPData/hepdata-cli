# -*- coding: utf-8 -*-

import pytest

from click.testing import CliRunner

from hepdata_cli.api import Client
from hepdata_cli.cli import cli


# arguments for testing

test_find_arguments = [
    ('reactions:"P P--> LQ LQ X"', None, None),
    ('reactions:"P P--> LQ LQ"', 'year', None),
    ('reactions:"P P--> LQ LQ"', 'arxiv', None),
    ('reactions:"P P--> LQ LQ"', None, 'arxiv'),
    ('reactions:"P P--> LQ LQ"', None, 'hepdata'),
    ('reactions:"P P"', None, 'hepdata'),
]


# api test

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


# cli testing

@pytest.mark.parametrize("query, keyword, ids", test_find_arguments)
def test_cli_find(query, keyword, ids):
    runner = CliRunner()
    result = runner.invoke(cli, ['find', query, '-kw', keyword, '-i', ids])
    assert result.exit_code == 0
