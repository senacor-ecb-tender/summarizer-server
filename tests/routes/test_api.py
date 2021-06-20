from fastapi.testclient import TestClient
from main import app
from routes.api import short_summaries, long_summaries

client = TestClient(app)


def test_get_index_returns_html():
    response = client.get("/")
    assert response.ok
    assert b'<!DOCTYPE html>' in response.content
    assert b'ECB Summarizer' in response.content


def test_that_upload_post_with_empty_form_returns_error():
    response = client.post("/upload")

    assert not response.ok
    assert response.status_code == 422
    assert b'"topic"],"msg":"field required","type":"value_error.missing"' in response.content
    assert b'"summary_type"],"msg":"field required","type":"value_error.missing"' in response.content
    assert b'"file"],"msg":"field required","type":"value_error.missing"' not in response.content #TODO bc file is optional for now


#TODO check if there are parameterized tests
def test_that_upload_post_returns_correct_summary():
    response = client.post("/upload", data={"topic": "pandemic", "summary_type": "short", "file": ""})
    assert short_summaries["pandemic"] in response.text
    response = client.post("/upload", data={"topic": "climate_risk", "summary_type": "long", "file": ""})
    assert long_summaries["climate_risk"] in response.text
