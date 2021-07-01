import logging
from typing import List

import torch
from pydantic import BaseSettings

from .model_loader import ModelManager
from .post_process import process
from .pipeline import filter_topic

logger = logging.getLogger(__name__)


class GenerationSettings(BaseSettings):
    # Pre-processing
    filter_topic: bool = False
    min_sentences_to_keep: int = 10
    window_size: int = 5

    # Default beam search parameters
    num_beams: int = 3
    length_penalty: float = 1.2
    no_repeat_ngram_size: int = 3
    early_stopping: bool = True

    class Config:
        env_file = '.generation'
        env_file_encoding = 'utf-8'


gen_settings = GenerationSettings()


class _SpecificSettings(BaseSettings):
    # Pre-processing
    filter_topic: bool = gen_settings.filter_topic
    min_sentences_to_keep: int = gen_settings.min_sentences_to_keep
    window_size: int = gen_settings.window_size

    # Default beam search parameters
    num_beams: int = gen_settings.num_beams
    length_penalty: float = gen_settings.length_penalty
    no_repeat_ngram_size: int = gen_settings.no_repeat_ngram_size
    early_stopping: bool = gen_settings.early_stopping


class ShortSettings(_SpecificSettings):
    min_length: int = 50
    max_length: int = 180

    class Config:
        env_prefix = 'short_'
        env_file = '.generation'
        env_file_encoding = 'utf-8'


class LongSettings(_SpecificSettings):
    min_length: int = 240
    max_length: int = 600

    class Config:
        env_prefix = 'long_'
        env_file = '.generation'
        env_file_encoding = 'utf-8'


short_settings = ShortSettings()
long_settings = LongSettings()


def predict(input_text: str, topic: str, summary_type: str, model_mgr: ModelManager) -> List[str]:
    logger.info(f'Creating {summary_type} summary for text of length {len(input_text)} and topic {topic}')
    settings = short_settings if summary_type == 'short' else long_settings

    if settings.filter_topic:
        input_text = filter_topic(text=input_text,
                                  topic=topic,
                                  window_size=settings.window_size,
                                  min_sentences=settings.min_sentences_to_keep)

    inputs = model_mgr.tokenizer.encode(text=input_text, return_tensors='pt')
    global_attention_mask = torch.zeros_like(inputs)
    global_attention_mask[:, 0] = 1

    outputs = model_mgr.model.generate(
        inputs,
        global_attention_mask=global_attention_mask,
        max_length=settings.max_length,
        min_length=settings.min_length,
        length_penalty=settings.length_penalty,
        num_beams=settings.num_beams,
        no_repeat_ngram_size=settings.no_repeat_ngram_size,
        early_stopping=settings.early_stopping
    )

    output_text = model_mgr.tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
    output_sentences = process(output_text)
    return output_sentences
