import pytest
from summarizer.routes import readiness
from fastapi import HTTPException
from fastapi.testclient import TestClient


def test_that_host_is_ready(mocker, mock_model, mock_tokenizer):
    mocker.patch.object(readiness.model_mgr, 'model', mock_model())
    assert readiness.get_readiness()['isReady'] == 'true'


def test_that_host_is_not_ready_without_model():
    with pytest.raises(HTTPException) as context:
        readiness.get_readiness()
        assert context.value.status_code == 503


def test_that_readiness_works_using_routing_pattern(mocker, mock_model, get_app):
    mocker.patch('summarizer.routes.readiness.model_mgr.model', mock_model)
    app = get_app()

    client = TestClient(app)

    response = client.get("/probes/healthz")
    assert response.ok

