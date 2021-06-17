from routes import api


def test_that_hello_work_works():
    assert api.index_html()['hello'] == 'world'
