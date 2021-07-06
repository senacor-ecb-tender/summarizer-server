def test_that_all_routes_are_included(get_app):
    app = get_app()

    routes = app.routes
    assert len(routes) == 12  # the first 4 routes are api descriptions such as swagger or redoc
    assert routes[4].name == 'index_html'
    assert routes[5].name == 'upload_file'
    assert routes[6].name == 'get_config'
    assert routes[7].name == 'get_readiness'
    assert routes[8].name == 'login'
    assert routes[9].name == 'get_frontend'
    assert routes[10].name == 'get_favicon'
    assert routes[11].name == 'get_static'
