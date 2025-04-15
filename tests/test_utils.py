import pytest  # noqa F401
from utils import load_pickle
from utils import find_filing


@pytest.mark.skip(reason="local use only")
def test_load_pickle():
    obj = load_pickle(cik="927972", accession_number="0001193125-04-182006")
    assert obj and obj.is_ready()


def test_find_filing():
    obj = find_filing(accession_number="0001193125-04-182006")
    assert obj
    assert obj["accession_number"] == "0001193125-04-182006"
    assert obj["cik"] == "927972"
    assert obj["company_name"] == "DLB FUND GROUP"
