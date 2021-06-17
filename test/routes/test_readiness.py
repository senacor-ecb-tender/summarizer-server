from routes import readiness


def test_that_host_is_ready():
    assert readiness.get_readiness()['isReady'] == 'true'
