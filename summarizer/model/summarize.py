import logging
from typing import List

import torch
from .model_loader import ModelManager
from .post_process import process
logger = logging.getLogger(__name__)


def predict(input_test: str, topic: str, summary_type: str, model_mgr: ModelManager) -> List[str]:
    logger.info(f'Creating {summary_type} summary for text of length {len(input_test)} and topic {topic}')
    (max_length, min_length) = (180, 50) if summary_type == 'short' else (600, 240)

    inputs = model_mgr.tokenizer.encode(text=input_test, return_tensors='pt')
    global_attention_mask = torch.zeros_like(inputs)
    global_attention_mask[:, 0] = 1

    outputs = model_mgr.model.generate(
        inputs,
        global_attention_mask=global_attention_mask,
        max_length=max_length,
        min_length=min_length,
        length_penalty=1.2,
        num_beams=3,
        no_repeat_ngram_size=3,
        early_stopping=True
    )

    output_text = model_mgr.tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
    output_sentences = process(output_text)
    return output_sentences
