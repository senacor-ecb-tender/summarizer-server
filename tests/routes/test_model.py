import pytest
from fastapi.testclient import TestClient
from tests.model.test_summarize import model, tokenizer


@pytest.mark.order(8)
def test_get_model_form_returns_html(mocker):
    mocker.patch('model.model_loader.fetch_model', return_value=(model, tokenizer))
    mocker.patch('routes.model.load_model_names', return_value=['test_model_1', 'test_model_2'])
    from main import app

    with TestClient(app) as client:
        response = client.get("/model")
        assert response.ok
        assert b'<!DOCTYPE html>' in response.content
        assert b'ECB Summarizer Model Loader' in response.content
        assert b'test_model_1' in response.content
        assert b'test_model_2' in response.content


@pytest.mark.order(9)
def test_post_model_form_without_params_returns_error(mocker):
    mocker.patch('model.model_loader.fetch_model', return_value=(model, tokenizer))
    from main import app

    with TestClient(app) as client:
        response = client.post("/model")
        assert not response.ok
        assert response.status_code == 422
        assert b'"model_name"],"msg":"field required","type":"value_error.missing"' in response.content
        assert b'"version"],"msg":"field required","type":"value_error.missing"' in response.content


@pytest.mark.order(10)
def test_post_model_form_returns_ok(mocker):
    mocker.patch('model.model_loader.fetch_model', return_value=(model, tokenizer))
    from main import app

    with TestClient(app) as client:
        response = client.post("/model", data={'model_name': 'model_1', 'version': 'version_1'})
        assert response.ok






