import logging
import pathlib
from typing import List

import torch
from pydantic import BaseSettings

from .model_loader import ModelManager
from .post_process import process
from .pre_process import filter_topic
from ..utils.tracing import traced

logger = logging.getLogger(__name__)

ENV_FILE = str(pathlib.Path(__file__).parent / '.generation')


class GenerationSettings(BaseSettings):
    # Pre-processing
    filter_topic: bool = False
    min_input_sentences: int = 20
    window_size: int = 7
    fraction_to_keep: float = 0.40

    # Default beam search parameters
    num_beams: int = 3
    length_penalty: float = 1.0
    no_repeat_ngram_size: int = 3
    early_stopping: bool = True

    # Post-processing
    cut_to_max_sentences: bool = False

    class Config:
        env_file = ENV_FILE
        env_file_encoding = 'utf-8'


gen_settings = GenerationSettings()


class _SpecificSettings(BaseSettings):
    # Pre-processing
    filter_topic: bool = gen_settings.filter_topic
    min_input_sentences: int = gen_settings.min_input_sentences
    window_size: int = gen_settings.window_size
    fraction_to_keep: float = gen_settings.fraction_to_keep

    # Default beam search parameters
    num_beams: int = gen_settings.num_beams
    length_penalty: float = gen_settings.length_penalty
    no_repeat_ngram_size: int = gen_settings.no_repeat_ngram_size
    early_stopping: bool = gen_settings.early_stopping

    # Post-processing
    cut_to_max_sentences: bool = gen_settings.cut_to_max_sentences

    # Length-specific settings
    min_length: int
    max_length: int
    min_sentences: int
    max_sentences: int


class ShortSettings(_SpecificSettings):
    min_length: int = 80
    max_length: int = 200

    min_sentences: int = 3
    max_sentences: int = 6

    class Config:
        env_prefix = 'short_'
        env_file = ENV_FILE
        env_file_encoding = 'utf-8'


class LongSettings(_SpecificSettings):
    min_length: int = 400
    max_length: int = 650

    min_sentences: int = 9
    max_sentences: int = 15

    class Config:
        env_prefix = 'long_'
        env_file = ENV_FILE
        env_file_encoding = 'utf-8'


short_settings = ShortSettings()
long_settings = LongSettings()


@traced
def predict(input_text: str, topic: str, summary_type: str, model_mgr: ModelManager) -> List[str]:
    logger.info(f'Creating {summary_type} summary for text of length {len(input_text)} and topic {topic}')
    settings = short_settings if summary_type == 'short' else long_settings

    if settings.filter_topic:
        input_text = filter_topic(text=input_text,
                                  topic=topic,
                                  window_size=settings.window_size,
                                  min_sentences=settings.min_input_sentences,
                                  fraction_to_keep=settings.fraction_to_keep)

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

    return decode_summary(outputs, model_mgr, settings)


@traced
def decode_summary(outputs: torch.Tensor, model_mgr: ModelManager, settings: _SpecificSettings) -> List[str]:
    output_text = model_mgr.tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
    sentences = process(output_text)

    if len(sentences) > settings.max_sentences:
        logger.warning(f"Produced too many sentences: {len(sentences)} instead of {settings.max_sentences} "
                       f"from {outputs[0].size()} tokens. Cutting enabled: {settings.cut_to_max_sentences}.")

        if settings.cut_to_max_sentences:
            sentences = sentences[:settings.max_sentences]

    if len(sentences) < settings.min_sentences:
        logger.warning(f"Produced too few sentences: {len(sentences)} instead of {settings.min_sentences} "
                       f"from {outputs[0].size()} tokens.")
    return sentences
