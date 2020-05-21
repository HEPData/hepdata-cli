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
    client.find(query, keyword, ids)
