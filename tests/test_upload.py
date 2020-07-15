# -*- coding: utf-8 -*-

import pytest
import os
import requests
import requests_mock

from click.testing import CliRunner

from hepdata_cli.api import Client
from hepdata_cli.cli import cli


# arguments for testing

test_upload_arguments = [
    (os.path.dirname(__file__) + "/SubmissionTestFiles/" + 'TestHEPSubmission.tar.gz', 'my@email.com', None, None, True, 'my_pswd'),
    (os.path.dirname(__file__) + "/SubmissionTestFiles/" + 'TestHEPSubmission.tar.gz', 'my@email.com', '123', None, True, 'my_pswd'),
    (os.path.dirname(__file__) + "/SubmissionTestFiles/" + 'TestHEPSubmission.tar.gz', 'my@email.com', '123', '0123456789', False, 'my_pswd'),
]


# api testing

@pytest.mark.parametrize('path_to_file, email, recid, invitation_cookie, sandbox, password', test_upload_arguments)
def test_api_upload(path_to_file, email, recid, invitation_cookie, sandbox, password):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://www.hepdata.net/ping', real_http=True)
        m.post('https://www.hepdata.net/record/cli_upload', text='hepdata_response')
        client = Client(verbose=True)
        client.upload(path_to_file, email, recid, invitation_cookie, sandbox, password)


# api testing  ---  HTTP Exception Handling

@pytest.mark.parametrize('path_to_file, email, recid, invitation_cookie, sandbox, password', test_upload_arguments)
def test_api_upload_HTTP_Exception(path_to_file, email, recid, invitation_cookie, sandbox, password):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://www.hepdata.net/ping', real_http=True)
        m.post('https://www.hepdata.net/record/cli_upload', text='hepdata_error_response', status_code=400)
        client = Client(verbose=True)
        with pytest.raises(requests.exceptions.HTTPError):
            client.upload(path_to_file, email, recid, invitation_cookie, sandbox, password)


# cli testing

@pytest.mark.parametrize('path_to_file, email, recid, invitation_cookie, sandbox, password', test_upload_arguments)
def test_cli_upload(path_to_file, email, recid, invitation_cookie, sandbox, password):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://www.hepdata.net/ping', real_http=True)
        m.post('https://www.hepdata.net/record/cli_upload', text='hepdata_response')
        runner = CliRunner()
        runner.invoke(cli, ['upload', path_to_file, '-e', email, '-r', recid, '-i', invitation_cookie, '-s', sandbox, '-p', password])
