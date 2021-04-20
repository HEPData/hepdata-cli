# -*- coding: utf-8 -*-

from .version import __version__
from .resilient_requests import resilient_requests

import tarfile
import sys
import re
import os
import errno

SITE_URL = "https://www.hepdata.net"
# SITE_URL = "http://127.0.0.1:5000"

UPLOAD_MAX_SIZE = 52000000  # Upload limit in bytes

MAX_MATCHES, MATCHES_PER_PAGE = (10000, 10) if "pytest" not in sys.modules else (144, 12)


class Client(object):
    """API class to handle all queries to HEPData."""

    def __init__(self, verbose=False):
        """
        Initialises the client object.

        :param verbose: prints additional output.
        """
        self.verbose = verbose
        self.version = __version__
        # check service availability
        resilient_requests('get', SITE_URL + '/ping')

    def find(self, query, keyword=None, ids=None, max_matches=MAX_MATCHES, matches_per_page=MATCHES_PER_PAGE):
        """
        Search function for the hepdata database. Calls hepdata.net search function.

        :param query: string passed to hepdata.net search function. See advanced search tips at hepdata.net.
        :param keyword: filters return dictionary for given keyword. Exact match is first attempted, otherwise partial match is accepted.
        :param ids: accepts one of ("arxiv", "inspire", "hepdata").

        :return: returns a list of (filtered if 'keyword' is specified) dictionaries for the search matches. If 'ids' is specified it instead returns a list of ids as a string.
        """
        find_results = []
        for counter in range(int(max_matches / matches_per_page)):
            counter += 1
            response = self._query(query, page=counter, size=matches_per_page)
            data = response.json()
            if len(data['results']) == 0:
                break
            elif keyword is None and ids is None:
                # return full list of dictionary
                find_results += data['results']
            else:
                assert ids in [None, "arxiv", "inspire", "hepdata", "id"], "allowd ids are: arxiv, inspire and hepdata"
                if ids is not None:
                    if ids == "hepdata":
                        ids = "id"
                    keyword = ids
                # return specific dictionary entry (exact match)
                if any([keyword in result.keys() for result in data['results']]):
                    if ids is None:
                        find_results += [{keyword: result[keyword]} for result in data['results'] if keyword in result.keys()]
                    else:
                        find_results += [str(result[keyword]).replace("arXiv:", "") for result in data['results'] if keyword in result.keys()]
                # return specific dictionary entry (partial match)
                elif any([any([keyword in key for key in result.keys()]) for result in data['results']]):
                    if ids is None:
                        find_results += [{key: result[key] for key in result.keys() if keyword in key} for result in data['results']]
                    else:
                        find_results += [[str(result[key]).replace("arXiv:", "") for key in result.keys() if keyword in key][0]
                                         if len([result[key] for key in result.keys() if keyword in key]) > 0 else "" for result in data['results']]
            if len(data['results']) < matches_per_page:
                break
        if ids is None:
            return find_results
        else:
            return ' '.join(find_results)

    def download(self, id_list, file_format=None, ids=None, table_name='', download_dir='./hepdata-downloads'):
        """
        Downloads from the hepdata database the specified records.

        :param id_list: list of ids to download. These can be obtained by the find function.
        :param file_format: accepts one of ('csv', 'root', 'yaml', 'yoda', 'json'). Specifies the download file format.
        :param ids: accepts one of ('inspire', 'hepdata'). It specifies what type of ids have been passed.
        :param table_name: restricts download to specific tables.
        :param download_dir: defaults to ./hepdata-downloads. Specifies where to download the files.
        """

        urls = self._build_urls(id_list, file_format, ids, table_name)
        for url in urls:
            if self.verbose is True:
                print("Downloading: " + url)
            download_url(url, download_dir)

    def fetch_names(self, id_list, ids=None):
        """
        Returns the names of the tables in the provided records. These are the possible inputs of table_name parameter in download function.

        :param id_list: list of id of records of which to return table names.
        :param ids: accepts one of ('inspire', 'hepdata'). It specifies what type of ids have been passed.
        """
        urls = self._build_urls(id_list, 'json', ids, '')
        table_names = []
        for url in urls:
            response = resilient_requests('get', url)
            json_dict = response.json()
            table_names += [[data_table['name'] for data_table in json_dict['data_tables']]]
        return table_names

    def upload(self, path_to_file, email, recid=None, invitation_cookie=None, sandbox=True, password=None):
        """
        Upload record.

        :param path_to_file: path of file to be uploaded.
        :param email: email address of existing HEPData user.
        :recid: HEPData ID (not the INSPIRE ID) of an existing record.
        :invitation_cookie: token sent in the invitation email for a non-sandbox record.
        :sandbox: True (default) or False if the file should be uploaded to the sandbox.
        :password: password of existing HEPData user (prompt if not specified).
        """
        file_size = os.path.getsize(path_to_file)
        assert file_size < UPLOAD_MAX_SIZE,\
            '{} too large ({} bytes > {} bytes)'.format(path_to_file, file_size, UPLOAD_MAX_SIZE)
        files = {'hep_archive': open(path_to_file, 'rb')}
        data = {'email': email, 'recid': recid, 'invitation_cookie': invitation_cookie, 'sandbox': sandbox, 'pswd': password}
        resilient_requests('post', SITE_URL + '/record/cli_upload', data=data, files=files)
        # print upload location
        if sandbox is True and recid is None:
            print('Uploaded ' + path_to_file + ' to a new record at ' + SITE_URL + '/record/sandbox')
        elif sandbox is True and recid is not None:
            print('Uploaded ' + path_to_file + ' to ' + SITE_URL + '/record/sandbox/' + str(recid))
        else:
            print('Uploaded ' + path_to_file + ' to ' + SITE_URL + '/record/' + str(recid))

    def _build_urls(self, id_list, file_format, ids, table_name):
        """Builds urls for download and fetch_names, given the specified parameters."""
        if type(id_list) not in (tuple, list):
            id_list = id_list.split()
        assert len(id_list) > 0, 'Ids are required.'
        assert file_format in ['csv', 'root', 'yaml', 'yoda', 'json'], "allowed formats are: csv, root, yaml, yoda and json."
        assert ids in ['inspire', 'hepdata'], "allowed ids are: inspire and hepdata."
        if table_name == '':
            params = {'format': file_format}
        else:
            params = {'format': file_format, 'table': table_name}
        urls = [resilient_requests('get', SITE_URL + '/record/' + ('ins' if ids == 'inspire' else '') + id_entry, params=params).url for id_entry in id_list]
        return urls

    def _query(self, query, page, size):
        """Builds the search query passed to hepdata.net."""
        url = SITE_URL + '/search/?q=' + query + '&format=json&page=' + str(page) + '&size=' + str(size)
        response = resilient_requests('get', url)
        if self.verbose is True:
            print('Looking up: ' + url)
        return response


def mkdir(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as exc:   # Guard against race condition (directory created between os.path.exists and os.makedirs)
            if exc.errno != errno.EEXIST:
                raise Exception


def download_url(url, download_dir):
    """Download file and if necessary extract it."""
    assert is_downloadable(url), "Given url is not downloadable: {}".format(url)
    response = resilient_requests('get', url, allow_redirects=True)
    if url[-4:] == 'json':
        filename = 'HEPData-' + url.split('/')[-1].split("?")[0] + ".json"
    else:
        filename = getFilename_fromCd(response.headers.get('content-disposition'))
    if filename[0] == '"' and filename[-1] == '"':
        filename = filename[1:-1]
    filepath = download_dir + "/" + filename
    mkdir(os.path.dirname(filepath))
    open(filepath, 'wb').write(response.content)
    if filepath.endswith("tar.gz") or filepath.endswith("tar"):
        tar = tarfile.open(filepath, "r:gz" if filepath.endswith("tar.gz") else "r:")
        tar.extractall(path=os.path.dirname(filepath))
        tar.close()
        os.remove(filepath)


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
    header = resilient_requests('head', url, allow_redirects=True).headers
    content_type = header.get('content-type')
    if 'html' in content_type.lower():
        return False
    return True
