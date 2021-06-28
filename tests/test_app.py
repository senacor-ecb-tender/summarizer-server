from tests.model.test_summarize import model, tokenizer
import pytest


@pytest.mark.order(3)
def test_that_all_routes_are_included(mocker):
    mocker.patch('model.model_loader.fetch_model', return_value=(model, tokenizer))
    from main import app
    routes = app.routes
    assert len(routes) == 9  # the first 4 routes are api descriptions such as swagger or redoc
    assert routes[4].name == 'index_html'
    assert routes[5].name == 'upload_file'
    assert routes[6].name == 'get_model_form'
    assert routes[7].name == 'load_model'
    assert routes[8].name == 'get_readiness'
