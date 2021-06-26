from typing import List
import pytest
from torch._tensor import Tensor


class MockTokenizer:
    def __init__(self):
        self.encode_called = False
        self.decode_called = False

    def encode(self, text: str, return_tensors: str) -> Tensor:
        self.encode_called = True
        return Tensor(1, 2, 3)

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


model = MockModel()
tokenizer = MockTokenizer()

@pytest.mark.order(1)
def test_that_short_summaries_work(mocker):
    mocker.patch('model.model_loader.fetch_model', return_value=(model, tokenizer))
    from model.summarize import predict
    predict('Some input text', 'some_topic', 'short')
    assert tokenizer.encode_called
    assert tokenizer.decode_called
    assert model.generate_called
    assert model.min_length == 50
    assert model.max_length == 180

@pytest.mark.order(2)
def test_that_long_summaries_work(mocker):
    from model.summarize import predict
    mocker.patch('model.model_loader.fetch_model', return_value=(model, tokenizer))

    predict('Some input text', 'some_topic', 'long')
    assert tokenizer.encode_called
    assert tokenizer.decode_called
    assert model.generate_called
    assert model.min_length == 240
    assert model.max_length == 600

