# -*- coding: utf-8 -*-

import requests
import re


class Client(object):

    def __init__(self, verbose):
        self.verbose = verbose

    def find(self, query):
        response = self._query(query)
        data = response.json()
        return data['results']

    def download(self, query, csv=False, root=False, yaml=False, yoda=False):
        results = self.find(query)
        for result in results:
            links = result['access_urls']['links']
            if csv is True:
                download_url(links['csv'])
            if root is True:
                download_url(links['root'])
            if yaml is True:
                download_url(links['yaml'])
            if yoda is True:
                download_url(links['yoda'])

    def _query(self, query):
        url = 'https://www.hepdata.net/search/?q=' + query + "&format=json"
        response = requests.get(url)
        if self.verbose is True:
            print("\nLooking up: " + url + "\n")
        return response


def download_url(url):
    assert is_downloadable(url), "Given url is not downloadable: {}".format(url)
    response = requests.get(url, allow_redirects=True)
    filename = getFilename_fromCd(response.headers.get('content-disposition'))
    open(filename, 'wb').write(response.content)


def getFilename_fromCd(cd):
    """Get filename from content-disposition."""
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]


def is_downloadable(url):
    """Does the url contain a downloadable resource?"""
    header = requests.head(url, allow_redirects=True).headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True
