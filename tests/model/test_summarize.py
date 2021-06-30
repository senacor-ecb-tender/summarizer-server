from model.model_loader import ModelManager
from summarizer.model.summarize import predict


def test_that_short_summaries_work(mocker, mock_model, mock_tokenizer):
    tokenizer = mock_tokenizer()
    model = mock_model()
    model_mgr = ModelManager.instance()
    mocker.patch.object(model_mgr, 'tokenizer', tokenizer)
    mocker.patch.object(model_mgr, 'model', model)

    predict('Some input text', 'some_topic', 'short', model_mgr)
    assert tokenizer.encode_called
    assert tokenizer.decode_called
    assert model.generate_called
    assert model.min_length == 50
    assert model.max_length == 180


def test_that_long_summaries_work(mocker, mock_model, mock_tokenizer):
    # TODO: Instead of mocking, a spy on the methods of interest should be sufficient
    tokenizer = mock_tokenizer()
    model = mock_model()
    model_mgr = ModelManager.instance()
    mocker.patch.object(model_mgr, 'tokenizer', tokenizer)
    mocker.patch.object(model_mgr, 'model', model)

    predict('Some input text', 'some_topic', 'long', model_mgr)
    assert tokenizer.encode_called
    assert tokenizer.decode_called
    assert model.generate_called
    assert model.min_length == 240
    assert model.max_length == 600
