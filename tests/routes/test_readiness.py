from tests.model.test_summarize import model, tokenizer
import pytest

@pytest.mark.order(7)
def test_that_host_is_ready(mocker):
    mocker.patch('model.model_loader.fetch_model', return_value=(model, tokenizer))
    from routes import readiness

    assert readiness.get_readiness()['isReady'] == 'true'
