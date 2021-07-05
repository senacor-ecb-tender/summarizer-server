import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient


def test_get_index_returns_html(get_app):
    app = get_app()

    client = TestClient(app)

    response = client.get("/")
    assert response.ok
    assert b'<!DOCTYPE html>' in response.content
    assert b'ECB Summarizer' in response.content


def test_that_upload_post_with_empty_form_returns_error(get_app):
    app = get_app()
    client = TestClient(app)

    response = client.post("/upload")

    assert not response.ok
    assert response.status_code == 422
    assert b'"topic"],"msg":"field required","type":"value_error.missing"' in response.content
    assert b'"summary_type"],"msg":"field required","type":"value_error.missing"' in response.content
    assert b'"file"],"msg":"field required","type":"value_error.missing"' in response.content


@pytest.mark.asyncio
async def test_that_upload_post_returns_correct_summary(mocker, get_app):
    def predict_mock(content, topic, summary_type, model_mgr):
        assert content != 'Test input'
        assert topic == 'pandemic'
        assert summary_type == 'short'
        return 'summary'

    mocker.patch('summarizer.routes.api.predict', predict_mock)
    app = get_app()

    async with AsyncClient(app=app, base_url="http://test") as client:
        f = '/tmp/fileupload'
        with open(f, 'wb') as tmp:
            tmp.write(b'Test input')
        response = await client.post("/upload",
                                     data={'topic': 'pandemic', "summary_type": "short"},
                                     files={'file': ("input_file.txt", f, "text/txt")})
        assert response.status_code == 200
        assert response.json() == {'result': 'summary'}
