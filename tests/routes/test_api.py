import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from fastapi import File
from tests.model.test_summarize import model, tokenizer


@pytest.mark.order(4)
def test_get_index_returns_html(mocker):
    mocker.patch('model.model_loader.fetch_model', return_value=(model, tokenizer))
    from main import app

    client = TestClient(app)

    response = client.get("/")
    assert response.ok
    assert b'<!DOCTYPE html>' in response.content
    assert b'ECB Summarizer' in response.content


@pytest.mark.order(5) # TODO: remove this smell -> serializes testing
def test_that_upload_post_with_empty_form_returns_error():
    from main import app
    client = TestClient(app)

    response = client.post("/upload")

    assert not response.ok
    assert response.status_code == 422
    assert b'"topic"],"msg":"field required","type":"value_error.missing"' in response.content
    assert b'"summary_type"],"msg":"field required","type":"value_error.missing"' in response.content
    assert b'"file"],"msg":"field required","type":"value_error.missing"' in response.content


# TODO check if there are parameterized tests
@pytest.mark.order(6)
@pytest.mark.asyncio
async def test_that_upload_post_returns_correct_summary(mocker):
    def predict_mock(content, topic, summary_type):
        assert content != 'Test input'
        assert topic == 'pandemic'
        assert summary_type == 'short'
        return 'summary'

    mocker.patch('routes.api.predict', predict_mock)
    from main import app
    async with AsyncClient(app=app, base_url="http://test") as client:
        f = '/tmp/fileupload'
        with open(f, 'wb') as tmp:
            tmp.write(b'Test input')
        response = await client.post("/upload",
                               data={'topic': 'pandemic', "summary_type": "short"},
                               files={'file': ("input_file.txt", f, "text/txt")})
        assert response.status_code == 200
        assert response.json() == {'result': 'summary'}


