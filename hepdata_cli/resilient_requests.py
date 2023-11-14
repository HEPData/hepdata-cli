# -*- coding: utf-8 -*-

from builtins import super

import requests
import sys

from requests.exceptions import HTTPError
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


DEFAULT_TIMEOUT = 295  # seconds
TOTAL_RETRIES = 5
DEBUG_FLAG = False


def exception_handler(exception_type, exception, traceback, debug_hook=sys.excepthook):
    if DEBUG_FLAG:
        debug_hook(exception_type, exception, traceback)
    else:
        print("%s: %s" % (exception_type.__name__, exception))


sys.excepthook = exception_handler


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


retry_strategy = Retry(total=TOTAL_RETRIES,
                       backoff_factor=2,
                       status_forcelist=[429, 500, 502, 503, 504],
                       allowed_methods=["GET", "POST"])
adapter = TimeoutHTTPAdapter(max_retries=retry_strategy)


def expanded_raise_for_status(res):
    """
    Take a "requests" response object and expand the raise_for_status method to return more helpful errors
    :param res:
    :return: None
    """
    try:
        res.raise_for_status()
    except HTTPError as e:
        try:
            raise HTTPError('{}\nReason: {}'.format(str(e), res.json()['message']))
        except ValueError:
            raise e
    return


def resilient_requests(func, *args, **kwargs):
    with requests.Session() as session:
        session.mount("https://", adapter)
        response = getattr(session, func)(*args, **kwargs)
        expanded_raise_for_status(response)
    return response
