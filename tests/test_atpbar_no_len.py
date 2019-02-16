# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

import atpbar

##__________________________________________________________________||
@pytest.fixture()
def mock_reporter(monkeypatch):
    ret = mock.Mock()
    return ret

@pytest.fixture(autouse=True)
def mock_find_reporter(monkeypatch, mock_reporter):
    ret = mock.Mock()
    ret.return_value = mock_reporter
    monkeypatch.setattr(atpbar.main, 'find_reporter', ret)
    return ret

##__________________________________________________________________||
class Iter(object):
    def __init__(self, content):
        self.content = content

    def __iter__(self):
        for e in self.content:
            yield e

##__________________________________________________________________||
content = [mock.sentinel.item1, mock.sentinel.item2, mock.sentinel.item3]

##__________________________________________________________________||
def test_atpbar_no_len(mock_reporter, caplog):
    iterable = Iter(content)

    ##
    returned = [ ]
    with caplog.at_level(logging.WARNING):
        for e in atpbar.atpbar(iterable):
            returned.append(e)

    ##
    assert content == returned

    ##
    assert not mock_reporter.report.call_args_list

    ##
    assert 2 == len(caplog.records)
    assert 'WARNING' == caplog.records[0].levelname
    assert 'length is unknown' in caplog.records[0].msg

##__________________________________________________________________||
