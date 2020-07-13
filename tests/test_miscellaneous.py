from hepdata_cli.api import is_downloadable, getFilename_fromCd


def test_is_downloadable():
    assert is_downloadable("https://www.google.com/") is False


def test_getFilename_fromCd_success():
    assert getFilename_fromCd("filename=HEPData-ins1309874-v1-csv.tar.gz") == 'HEPData-ins1309874-v1-csv.tar.gz'


def test_getFilename_fromCd_None1():
    assert getFilename_fromCd("") is None


def test_getFilename_fromCd_None2():
    assert getFilename_fromCd("file=HEPData-ins1309874-v1-csv.tar.gz") is None
