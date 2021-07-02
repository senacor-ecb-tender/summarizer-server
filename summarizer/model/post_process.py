import logging
import re
from typing import List

import nltk

from ..utils.tracing import traced

logger = logging.getLogger(__name__)

END_OF_SENTENCE = r".?[.!?][\"']?"


@traced
def process(input_text: str) -> List[str]:
    # split into sentences
    sentences = nltk.sent_tokenize(input_text)
    pretty_sentences = list(map(prettify, sentences))

    if re.match(END_OF_SENTENCE, pretty_sentences[-1][-2:]) is None:
        pretty_sentences = pretty_sentences[:-1]

    return pretty_sentences


def prettify(sentence: str) -> str:
    return sentence.strip().capitalize().replace('\n', '').replace('  ', ' ') if sentence is not None else None


@traced
def download_dict():
    nltk.download('punkt', download_dir='cache')


if __name__ == "__main__":
    download_dict()
