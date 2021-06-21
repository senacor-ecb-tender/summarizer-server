from transformers import LEDTokenizer, LEDForConditionalGeneration, LEDConfig, AutoModelForSeq2SeqLM, AutoTokenizer
import torch

#model = LEDForConditionalGeneration.from_pretrained('allenai/led-base-16384', cache_dir="cache")
#tokenizer = LEDTokenizer.from_pretrained('allenai/led-base-16384', cache_dir="cache")
model = AutoModelForSeq2SeqLM.from_pretrained("allenai/led-base-16384", cache_dir="cache")
tokenizer = AutoTokenizer.from_pretrained("allenai/led-base-16384", cache_dir="cache")


def predict(input_test: str, topic: str, summary_type: str):
    max_length = 200 if summary_type == 'short' else 600
    inputs = tokenizer.encode(input_test, return_tensors='pt')
    global_attention_mask = torch.zeros_like(inputs)
    global_attention_mask[:, 0] = 1

    outputs = model.generate(
        inputs,
        global_attention_mask=global_attention_mask,
        max_length=180,
        min_length=50,
        length_penalty=1.2,
        num_beams=3,
        early_stopping=True
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)
