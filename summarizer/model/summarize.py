import logging
import torch
from .model_loader import fetch_model

logger = logging.getLogger(__name__)
model, tokenizer = fetch_model()


def predict(input_test: str, topic: str, summary_type: str):
    logging.info(f'Creating ${summary_type} summary for text of length ${len(input_test)} and topic ${topic}')
    (max_length, min_length) = (180, 50) if summary_type == 'short' else (600, 240)

    inputs = tokenizer.encode(input_test, return_tensors='pt')
    global_attention_mask = torch.zeros_like(inputs)
    global_attention_mask[:, 0] = 1

    outputs = model.generate(
        inputs,
        global_attention_mask=global_attention_mask,
        max_length=max_length,
        min_length=min_length,
        length_penalty=1.2,
        num_beams=3,
        no_repeat_ngram_size=3,
        early_stopping=True
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)
