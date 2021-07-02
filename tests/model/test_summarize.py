from summarizer.model.model_loader import ModelManager
from summarizer.model.summarize import predict, short_settings, long_settings


def test_that_summary_generation_works(mocker, mock_model, mock_tokenizer):
    model_mgr = ModelManager.instance()
    tokenizer = mocker.patch.object(model_mgr, 'tokenizer', mock_tokenizer())
    model = mocker.patch.object(model_mgr, 'model', mock_model())
    process = mocker.patch('summarizer.model.summarize.process')

    predict('Some input text', 'pandemic', 'short', model_mgr)

    assert tokenizer.encode_called
    assert model.generate_called
    assert tokenizer.decode_called
    assert process.called
    assert model.min_length == short_settings.min_length
    assert model.max_length == short_settings.max_length


def test_that_settings_are_honored(mocker, mock_model, mock_tokenizer):
    model_mgr = ModelManager.instance()
    mocker.patch.object(model_mgr, 'tokenizer', mock_tokenizer())
    model = mocker.patch.object(model_mgr, 'model', mock_model())
    mocker.patch('summarizer.model.summarize.decode_summary')

    predict('Some input text', 'pandemic', 'short', model_mgr)

    assert model.generate_called
    assert model.min_length == short_settings.min_length
    assert model.max_length == short_settings.max_length

    predict('Some input text', 'pandemic', 'long', model_mgr)

    assert model.generate_called
    assert model.min_length == long_settings.min_length
    assert model.max_length == long_settings.max_length
