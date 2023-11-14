# -*- coding: utf-8 -*-

import pytest
import requests

from hepdata_cli.resilient_requests import TimeoutHTTPAdapter, retry_strategy
from hepdata_cli.api import SITE_URL


def test_timeout():
    retry_strategy.total = 2
    adapter = TimeoutHTTPAdapter(max_retries=retry_strategy, timeout=0.0001)
    with requests.Session() as session:
        session.mount("https://", adapter)
        with pytest.raises(requests.exceptions.ConnectionError):
            session.get(SITE_URL + '/ping')
