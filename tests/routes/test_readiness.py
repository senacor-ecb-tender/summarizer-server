import pytest
from summarizer.routes import readiness
from fastapi import HTTPException


def test_that_host_is_ready(mocker, mock_model, mock_tokenizer):
    mocker.patch.object(readiness.model_mgr, '_model', mock_model())
    assert readiness.get_readiness()['isReady'] == 'true'


def test_that_host_is_not_ready_without_model():
    with pytest.raises(HTTPException) as context:
        readiness.get_readiness()
        assert context.value.status_code == 503
