import pytest
import torch
from typing import List


@pytest.fixture
def get_app(mocker, mock_model, mock_tokenizer):
    mocker.patch('summarizer.model.model_loader.fetch_model', return_value=(mock_model(), mock_tokenizer()))

    def _get():
        from summarizer.main import app
        return app

    return _get


class MockTokenizer:
    def __init__(self):
        self.encode_called = False
        self.decode_called = False

    def encode(self, text: str, return_tensors: str) -> torch.Tensor:
        self.encode_called = True
        return torch.Tensor(1, 2, 3)

    def decode(self, token_ids: List[int], skip_special_tokens: bool, clean_up_tokenization_spaces: bool):
        self.decode_called = True


class MockModel:
    def __init__(self):
        self.generate_called = False
        self.max_length = -1
        self.min_length = -1

    def generate(self,
                 inputs,
                 global_attention_mask,
                 max_length,
                 min_length,
                 length_penalty,
                 num_beams,
                 no_repeat_ngram_size,
                 early_stopping):
        self.generate_called = True
        self.max_length = max_length
        self.min_length = min_length
        return [inputs]


@pytest.fixture
def mock_model():
    def _create():
        return MockModel()

    return _create


@pytest.fixture
def mock_tokenizer():
    def _create():
        return MockTokenizer()

    return _create
