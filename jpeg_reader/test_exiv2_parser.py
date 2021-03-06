import subprocess

from .exiv2_parser import Exiv2Parser


class MockPopen(object):
    """Mock Popen method"""
    def __init__(self, cmd, *, stdout):
        pass

    def communicate(self):
        """Mock communicate method of Popen"""
        return b'bash: command not found: exiv2', b''


class MockPopenSuccess(MockPopen):
    def __init__(self, cmd, *, stdout):
        MockPopen.__init__(self, cmd, stdout=stdout)

    def communicate(self):
        """Mock communicate method of Popen"""
        return b'exiv2 0.26 001a00 (64 bit build)', b''


def test_get_version_fail(mocker, monkeypatch):
    monkeypatch.setattr(subprocess, 'Popen', MockPopen)
    version_info = Exiv2Parser.get_exiv2_version()
    assert version_info is None


def test_get_version_success(mocker, monkeypatch):
    monkeypatch.setattr(subprocess, 'Popen', MockPopenSuccess)
    version, commit = Exiv2Parser.get_exiv2_version()
    assert version == '0.26'
    assert commit == '001a00'



