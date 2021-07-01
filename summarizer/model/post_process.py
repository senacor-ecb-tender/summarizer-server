import logging
from typing import List

import nltk

from ..utils.tracing import traced

logger = logging.getLogger(__name__)


@traced
def process(input_text: str) -> List[str]:
    # split into sentences
    sentences = nltk.sent_tokenize(input_text)
    return list(map(prettify, sentences))


def prettify(sentence: str) -> str:
    return sentence.strip().capitalize().replace('\n', '').replace('  ', ' ') if sentence is not None else None


@traced
def download_dict():
    nltk.download('punkt', download_dir='cache')


if __name__ == "__main__":
    download_dict()
