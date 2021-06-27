import pytest


def test_that_host_is_ready():
    from summarizer.routes import readiness

    assert readiness.get_readiness()['isReady'] == 'true'
