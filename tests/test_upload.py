# -*- coding: utf-8 -*-

import pytest
import os
import shutil
import requests_mock

from click.testing import CliRunner

from hepdata_cli.api import Client
from hepdata_cli.cli import cli


# arguments for testing

test_upload_arguments = [
    (os.path.dirname(__file__) + "/" + 'TestHEPSubmission.tar.gz', 'my@email.com', None, None, True),
    (os.path.dirname(__file__) + "/" + 'TestHEPSubmission.tar.gz', 'my@email.com', '278', '8232e07f-d1d8-4883-bb1d-77fd9994ce4f', False),
]


# api testing

@pytest.mark.parametrize('path_to_file, email, recid, invitation_cookie, sandbox', test_upload_arguments)
def test_api_upload(path_to_file, email, recid, invitation_cookie, sandbox):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://www.hepdata.net/ping', real_http=True)
        m.register_uri('GET', 'http://www.hepdata.net/ping', real_http=True)
        m.post('http://www.hepdata.net/record/sandbox/upload', text='sandbox_response')
        m.post('http://www.hepdata.net/record/upload', text='response')
        client = Client(verbose=True)
        client.upload(path_to_file, email, recid, invitation_cookie, sandbox)


# cli testing

@pytest.mark.parametrize('path_to_file, email, recid, invitation_cookie, sandbox', test_upload_arguments)
def test_cli_upload(path_to_file, email, recid, invitation_cookie, sandbox):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://www.hepdata.net/ping', real_http=True)
        m.register_uri('GET', 'http://www.hepdata.net/ping', real_http=True)
        m.post('http://www.hepdata.net/record/sandbox/upload', text='sandbox_response')
        m.post('http://www.hepdata.net/record/upload', text='response')
        runner = CliRunner()
        runner.invoke(cli, ['upload', path_to_file, '-e', email, '-r', recid, '-i', invitation_cookie, '-s', sandbox])
