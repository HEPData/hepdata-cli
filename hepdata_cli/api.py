# -*- coding: utf-8 -*-

import requests
import re


class Client(object):

    def __init__(self, verbose=False):
        self.verbose = verbose

    def find(self, query, keyword=None, ids=None):
        response = self._query(query)
        data = response.json()
        if keyword is None and ids is None:
            # return full list of dictionary
            return data['results']
        else:
            assert ids in [None, "arxiv", "inspire", "hepdata"], "allowd ids are: arxiv, inspire and hepdata"
            if ids is not None:
                if ids == "hepdata":
                    ids = "id"
                keyword = ids
            # return specific dictionary entry (exact match)
            if any([keyword in result.keys() for result in data['results']]):
                if ids is None:
                    return [{keyword: result[keyword]} for result in data['results'] if keyword in result.keys()]
                else:
                    return " ".join([str(result[keyword]).replace("arXiv:", "") for result in data['results'] if keyword in result.keys()])
            # return specific dictionary entry (partial match)
            elif any([any([keyword in key for key in result.keys()]) for result in data['results']]):
                if ids is None:
                    return [{key: result[key] for key in result.keys() if keyword in key} for result in data['results']]
                else:
                    return " ".join([[str(result[key]).replace("arXiv:", "") for key in result.keys() if keyword in key][0]
                                     if len([result[key] for key in result.keys() if keyword in key]) > 0 else "" for result in data['results']])

    def download(self, id_list, file_format=None, ids=None, table=None):
        assert len(id_list) > 0, 'Ids are required for download.'
        assert file_format in ['csv', 'root', 'yaml', 'yoda', 'json'], "allowed formats are: csv, root, yaml, yoda and json."
        assert ids in ['inspire', 'hepdata'], "allowed ids are: inspire and hepdata."
        if table is None:
            params = {'format': file_format}
        else:
            params = {'format': file_format, 'table': "Table" + str(table)}
        for id_entry in id_list:
            url = requests.get('https://www.hepdata.net/record/' + ('ins' if ids == 'inspire' else '') + id_entry, params=params).url
            if self.verbose is True:
                print("Downloading: " + url)
            download_url(url)

    def _query(self, query):
        url = 'https://www.hepdata.net/search/?q=' + query + "&format=json"
        response = requests.get(url)
        if self.verbose is True:
            print("Looking up: " + url)
        return response


def download_url(url):
    assert is_downloadable(url), "Given url is not downloadable: {}".format(url)
    response = requests.get(url, allow_redirects=True)
    if url[-4:] == 'json':
        filename = 'HEPData-' + url.split('/')[-1].split("?")[0] + ".json"
    else:
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
    if 'html' in content_type.lower():
        return False
    return True
