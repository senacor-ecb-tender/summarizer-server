import pytest
from summarizer.model.post_process import prettify


@pytest.mark.parametrize('ugly,pretty', [
    ('   this is a sentence with \n newlines and a small first letter in it.  ', 'This is a sentence with newlines and a small first letter in it.'),
    ('  ', ''),
    (None, None),
    ])
def test_that_prettify_works(ugly, pretty):
    assert prettify(ugly) == pretty

