import logging
import re
from typing import List

import nltk

from ..utils.tracing import traced

logger = logging.getLogger(__name__)

END_OF_SENTENCE = r".?[.!?][\"']?"


@traced
def process(input_text: str) -> List[str]:
    sentences = nltk.sent_tokenize(input_text)
    pretty_sentences = list(map(prettify, sentences))

    if re.match(END_OF_SENTENCE, pretty_sentences[-1][-2:]) is None:
        pretty_sentences = pretty_sentences[:-1]

    return pretty_sentences


def prettify(sentence: str) -> str:
    sentence = sentence.strip()
    if not sentence:
        return sentence

    # if sentence starts with quote char, leave it
    if sentence[0] in ("'", '"'):
        start = sentence[0]
        sentence = sentence[1:]
    else:
        start = ""

    # remove newlines and multiple spaces
    sentence = sentence.replace("\n", " ")
    sentence = re.sub(r"\s+", " ", sentence)

    # capitalize first letter
    sentence = sentence[0].capitalize() + sentence[1:]

    # capitalize remaining "I"'s
    sentence = re.sub(r"\si\W", " I ", sentence)

    return start + sentence


@traced
def download_dict():
    nltk.download('punkt', download_dir='cache')


if __name__ == "__main__":
    download_dict()
