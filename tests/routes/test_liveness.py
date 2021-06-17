from routes import liveness
from socket import gethostname


def test_that_liveness_yields_hostname():
    assert liveness.get_liveness()['hostname'] == gethostname()
