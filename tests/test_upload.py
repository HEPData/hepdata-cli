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
    (os.path.dirname(__file__) + "/SubmissionTestFiles/" + 'TestHEPSubmission.tar.gz', 'my@email.com', None, None, True),
    (os.path.dirname(__file__) + "/SubmissionTestFiles/" + 'TestHEPSubmission.tar.gz', 'my@email.com', '123', None, True),
    (os.path.dirname(__file__) + "/SubmissionTestFiles/" + 'TestHEPSubmission.tar.gz', 'my@email.com', '123', '0123456789', False),
]


# api testing

@pytest.mark.parametrize('path_to_file, email, recid, invitation_cookie, sandbox', test_upload_arguments)
def test_api_upload(path_to_file, email, recid, invitation_cookie, sandbox):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://www.hepdata.net/ping', real_http=True)
        if sandbox is True:
            if recid is None:
                m.post('https://www.hepdata.net/record/sandbox/consume', text='sandbox_response')
            else:
                m.post('https://www.hepdata.net/record/sandbox/' + recid + '/consume', text='response')
        else:
            m.post('https://www.hepdata.net/record/' + recid + '/consume', text='response')
        client = Client(verbose=True)
        client.upload(path_to_file, email, recid, invitation_cookie, sandbox)


# api testing  ---  HTTP Exception Handling

@pytest.mark.parametrize('path_to_file, email, recid, invitation_cookie, sandbox', test_upload_arguments)
def test_api_upload_HTTP_Exception(path_to_file, email, recid, invitation_cookie, sandbox):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://www.hepdata.net/ping', real_http=True)
        if sandbox is True:
            if recid is None:
                m.post('https://www.hepdata.net/record/sandbox/consume', text='!!!Error Reason Sandbox Consume!!!', status_code=400)
            else:
                m.post('https://www.hepdata.net/record/sandbox/' + recid + '/consume', text='!!!Error Reason Sandbox Recid Consume!!!', status_code=400)
        else:
            m.post('https://www.hepdata.net/record/' + recid + '/consume', text='!!!Error Reason Record Recid Consume!!!', status_code=400)
        client = Client(verbose=True)
        try:
            client.upload(path_to_file, email, recid, invitation_cookie, sandbox)
        except requests.exceptions.HTTPError:
            print("Success!")


# cli testing

@pytest.mark.parametrize('path_to_file, email, recid, invitation_cookie, sandbox', test_upload_arguments)
def test_cli_upload(path_to_file, email, recid, invitation_cookie, sandbox):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://www.hepdata.net/ping', real_http=True)
        if sandbox is True:
            if recid is None:
                m.post('https://www.hepdata.net/record/sandbox/consume', text='sandbox_response')
            else:
                m.post('https://www.hepdata.net/record/sandbox/' + recid + '/consume', text='response')
        else:
            m.post('https://www.hepdata.net/record/' + recid + '/consume', text='response')
        runner = CliRunner()
        runner.invoke(cli, ['upload', path_to_file, '-e', email, '-r', recid, '-i', invitation_cookie, '-s', sandbox])
