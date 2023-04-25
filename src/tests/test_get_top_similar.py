import pytest
from .. import helper

@pytest.fixture
def test_get_top_similar_data():
    test_query = "I am a test query"
    test_strings = ["I am a test string", "I am a test string 2", "I am a test string 3"]

    return test_query, test_strings

def test_get_top_similar(test_get_top_similar_data):
    test_query, test_strings = test_get_top_similar_data
    test_k = 2
    test_get_top_similar = helper.get_top_similar.GetTopSimilar(strings=test_strings)
    result = test_get_top_similar.get_top_similar(test_query, test_k)

    assert len(result) == test_k, "Result length does not match k"