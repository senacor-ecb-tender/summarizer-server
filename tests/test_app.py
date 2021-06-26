

def test_that_all_routes_are_included(mocker):
    mocker.patch('model.model_loader.fetch_model', return_value=(None, None))
    from main import app
    routes = app.routes
    assert len(routes) == 8  # the first 4 routes are api descriptions such as swagger or redoc
    assert routes[4].name == 'index_html'
    assert routes[5].name == 'upload_file'
    assert routes[6].name == 'get_readiness'
    assert routes[7].name == 'get_liveness'
