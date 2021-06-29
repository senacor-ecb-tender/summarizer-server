import pytest


@pytest.mark.skip
def test_that_short_summaries_work(mocker, mock_model, mock_tokenizer):
    tokenizer = mock_tokenizer()
    model = mock_model()
    mocker.patch('summarizer.model.model_loader.fetch_model', return_value=(model, tokenizer))

    from summarizer.model.summarize import predict
    predict('Some input text', 'some_topic', 'short')
    assert tokenizer.encode_called
    assert tokenizer.decode_called
    assert model.generate_called
    assert model.min_length == 50
    assert model.max_length == 180


@pytest.mark.skip
def test_that_long_summaries_work(mocker, mock_model, mock_tokenizer):
    # TODO: Instead of mocking, a spy on the methods of interest should be sufficient
    tokenizer = mock_tokenizer()
    model = mock_model()
    mocker.patch('summarizer.model.model_loader.fetch_model', return_value=(model, tokenizer))
    from summarizer.model.summarize import predict

    predict('Some input text', 'some_topic', 'long')
    assert tokenizer.encode_called
    assert tokenizer.decode_called
    assert model.generate_called
    assert model.min_length == 240
    assert model.max_length == 600
