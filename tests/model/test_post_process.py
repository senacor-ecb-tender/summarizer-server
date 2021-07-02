import pytest

from summarizer.model.post_process import prettify, process


@pytest.mark.parametrize('ugly,pretty', [
    ('   this is a sentence with \n newlines and a small first letter in it.  ',
     'This is a sentence with newlines and a small first letter in it.'),
    ('  ', '')
])
def test_that_prettify_works(ugly, pretty):
    assert prettify(ugly) == pretty


def test_that_complete_sentences_remain():
    text = "This is a text. It is quite ugly!"
    assert process(text) == ["This is a text.", "It is quite ugly!"]


def test_that_only_whole_sentences_remain():
    text = "This is a text. It is quite ugly? And then it just"
    assert process(text) == ["This is a text.", "It is quite ugly?"]


def test_that_prettify_handles_quotation_marks():
    text = "'how come you don't notice the quote?'"
    assert prettify(text) == "'How come you don't notice the quote?'"


def test_that_prettify_capitalizes_i():
    text = "this is a text where i don't care, even though i'm concerned."
    assert prettify(text) == "This is a text where I don't care, even though I'm concerned."


def test_that_spaces_around_parentheses_are_cleaned():
    text = "this is [ a text ] where there are (spaces around )."
    assert prettify(text) == "This is [a text] where there are (spaces around)."
