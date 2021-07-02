import pytest
from summarizer.model.post_process import prettify, process


@pytest.mark.parametrize('ugly,pretty', [
    ('   this is a sentence with \n newlines and a small first letter in it.  ', 'This is a sentence with newlines and a small first letter in it.'),
    ('  ', ''),
    (None, None),
    ])
def test_that_prettify_works(ugly, pretty):
    assert prettify(ugly) == pretty


def test_that_complete_sentences_remain():
    text = "This is a text. It is quite ugly!"
    assert process(text) == ["This is a text.",  "It is quite ugly!"]


def test_that_only_whole_sentences_remain():
    text = "This is a text. It is quite ugly? And then it just"
    assert process(text) == ["This is a text.",  "It is quite ugly?"]
