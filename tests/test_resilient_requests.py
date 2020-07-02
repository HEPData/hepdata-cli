# -*- coding: utf-8 -*-

import requests

from hepdata_cli.resilient_requests import TimeoutHTTPAdapter, retry_strategy
from hepdata_cli.api import SITE_URL


def test_timeout():
    retry_strategy.total = 2
    adapter = TimeoutHTTPAdapter(max_retries=retry_strategy, timeout=0.0001)
    with requests.Session() as session:
        session.mount("https://", adapter)
        try:
            session.get(SITE_URL + '/ping')
        except requests.exceptions.ConnectTimeout:
            pass
