# -*- coding: utf-8 -*-

import pytest

from hepdata_cli.api import Client


@pytest.mark.parametrize(
    "query, keyword, ids",
    [
        ('reactions:"P P--> LQ LQ X"', None, None),
        ('reactions:"P P--> LQ LQ"', 'year', None),
        ('reactions:"P P--> LQ LQ"', None, 'arxiv'),
    ]
)
def test_find(query, keyword, ids):
    client = Client()
    search_result = client.find(query, keyword, ids)
    if ids is None:
        assert type(search_result) is list
        if len(search_result) > 0:
            assert all([type(entry) is dict for entry in search_result])
    else:
        assert type(search_result) is str


@pytest.mark.parametrize(
    "id_list, file_format, ids, table",
    [
        (["73322"], "json", "hepdata", None),
        (["1222326", "1694381", "1462258", "1309874"], "csv", "inspire", None),
        (["61434"], "yaml", "hepdata", 1),
    ]
)
def test_download(id_list, file_format, ids, table):
    client = Client()
    client.download(id_list, file_format, ids, table)
