# -*- coding: utf-8 -*-

import requests


class Client(object):

    def __init__(self, verbose):
        self.verbose = verbose

    def find(self, query):
        response = self._query(query)
        data = response.json()
        return data['results']

    def _query(self, query):
        url = 'https://www.hepdata.net/search/?q=' + query + "&format=json"
        response = requests.get(url)
        if self.verbose is True:
            print("\nLooking up: " + url + "\n")
        return response
