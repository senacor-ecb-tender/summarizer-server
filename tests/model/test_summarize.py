from unittest.mock import PropertyMock

from summarizer.model.model_loader import ModelManager
from summarizer.model import summarize
from summarizer.model.summarize import predict, short_settings, long_settings, filter_topic


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


def test_summarization_with_pre_filtering(mocker, mock_model, mock_tokenizer):
    model_mgr = ModelManager.instance()
    mocker.patch.object(model_mgr, 'tokenizer', mock_tokenizer())
    model = mocker.patch.object(model_mgr, 'model', mock_model())
    mocker.patch('summarizer.model.summarize.decode_summary')

    spy_on_filter = mocker.spy(summarize, 'filter_topic')

    mocker.patch.object(short_settings, 'filter_topic',
                        new_callable=PropertyMock(return_value=True))
    mocker.patch.object(short_settings, 'min_input_sentences',
                        new_callable=PropertyMock(return_value=2))
    mocker.patch.object(short_settings, 'window_size',
                        new_callable=PropertyMock(return_value=3))

    text = "Some input text. With multiple sentences. And another one. \
            And more context. And more text. And much more. So boring!"
    predict(text,
            "pandemic", "short", model_mgr)

    assert model.generate_called
    spy_on_filter.assert_called_once_with(text=text, topic="pandemic",
                                          window_size=3, min_sentences=2)



