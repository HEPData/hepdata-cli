# -*- coding: utf-8 -*-

import pytest
import os
import shutil
import tarfile
import tempfile
from unittest.mock import patch

from click.testing import CliRunner

from hepdata_cli.api import Client, download_url, mkdir
from hepdata_cli.cli import cli


# initial clean up

def cleanup(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    assert len(os.listdir(directory)) == 0
    os.rmdir(directory)


test_download_dir = './.pytest_downloads/'
mkdir(test_download_dir)  # in case it is not there
cleanup(test_download_dir)


# arguments for testing

test_api_download_arguments = [
    (["73322"], "json", "hepdata", ''),
    (["1222326", "1694381", "1462258", "1309874"], "csv", "inspire", ''),
    (["61434"], "yaml", "hepdata", "Table1"),
    (["1762350"], "yoda", "inspire", "Number density and Sum p_T pT>0.15 GeV/c"),
    (["2862529"], "yoda.h5", "inspire", "95% CL upper limit on XSEC times BF"),
    (["2862529"], "yoda.h5", "inspire", '')
]

test_cli_download_arguments = [
    (["2862529"], "json", "inspire", ''),
    (["1222326", "1694381", "1462258", "1309874"], "root", "inspire", ''),
    (["61434"], "yaml", "hepdata", "Table2"),
]


# api testing

@pytest.mark.parametrize("id_list, file_format, ids, table", test_api_download_arguments)
def test_api_download(id_list, file_format, ids, table):
    test_download_dir = './.pytest_downloads/'
    mkdir(test_download_dir)
    assert len(os.listdir(test_download_dir)) == 0
    client = Client(verbose=True)
    path_map = client.download(id_list, file_format, ids, table, test_download_dir)
    file_paths = [fp for fps in path_map.values() for fp in fps]
    assert len(os.listdir(test_download_dir)) > 0
    assert all(os.path.exists(fp) for fp in file_paths)
    cleanup(test_download_dir)


# cli testing

@pytest.mark.parametrize("id_list, file_format, ids, table", test_cli_download_arguments)
def test_cli_download(id_list, file_format, ids, table):
    test_download_dir = './.pytest_downloads/'
    mkdir(test_download_dir)
    assert len(os.listdir(test_download_dir)) == 0
    runner = CliRunner()
    result = runner.invoke(cli, ['download'] + id_list + ['-f', file_format, '-i', ids, '-t', table, '-d', test_download_dir])
    assert result.exit_code == 0
    assert len(os.listdir(test_download_dir)) > 0
    cleanup(test_download_dir)


# utility function testing

@pytest.mark.parametrize("files_raises", [{"file": "test.txt", "raises": False},
                                          {"file": "../test.txt", "raises": True},
                                          {"file": None, "raises": True}])
def test_tar_unpack(files_raises):
    """
    Test the unpacking of a tarfile
    """
    filename = files_raises["file"]
    raises = files_raises["raises"]
    if filename is None:  # To hit FileNotFoundError branch
        filename = 'test.txt'
        real_exists = os.path.exists
        def mock_exists(path):
            if path.endswith(filename):
                return False
            return real_exists(path)
        exists_patcher = patch('os.path.exists', mock_exists)
        exists_patcher.start()

    # Create a some tarfile with known content
    with tempfile.NamedTemporaryFile(delete=False, suffix='.tar.gz') as tmp:
        tar_path = tmp.name
    with tarfile.open(tar_path, "w:gz") as tar:
        info = tarfile.TarInfo(name=filename)
        content = b"Hello, World!"
        info.size = len(content)
        temp_content_file = tempfile.NamedTemporaryFile(delete=False)
        try:
            temp_content_file.write(content)
            temp_content_file.close()
            tar.add(temp_content_file.name, arcname=filename)
        finally:
            os.remove(temp_content_file.name)

    test_download_dir = './.pytest_downloads/'
    mkdir(test_download_dir)
    assert len(os.listdir(test_download_dir)) == 0

    # Mock the requests part to return our tarfile
    with patch('hepdata_cli.api.is_downloadable', return_value=True), \
         patch('hepdata_cli.api.resilient_requests') as mock_requests, \
         patch('hepdata_cli.api.getFilename_fromCd', return_value='test.tar.gz'):

        mock_response = mock_requests.return_value
        mock_response.content = open(tar_path, 'rb').read()
        mock_response.headers = {'content-disposition': 'filename=test.tar.gz'}

        # Test the download_url function
        try:
            if raises:
                with pytest.raises(Exception):
                    files = download_url('http://example.com/test.tar.gz', test_download_dir)
            else:
                files = download_url('http://example.com/test.tar.gz', test_download_dir)
                assert len(files) == 1
                for f in files:
                    assert os.path.exists(f)
                    with open(f, 'rb') as fr:
                        assert fr.read() == b"Hello, World!"
        finally:
            exists_patcher.stop() if filename is None else None
            if os.path.exists(tar_path):
                os.remove(tar_path)
            cleanup(test_download_dir)
