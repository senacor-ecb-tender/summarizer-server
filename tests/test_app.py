from main import app


def test_that_all_routes_are_included():
    routes = app.routes
    assert len(routes) == 7 # the first 4 routes are api descriptions such as swagger or redoc
    assert routes[4].name == 'index_html'
    assert routes[5].name == 'get_readiness'
    assert routes[6].name == 'get_liveness'
