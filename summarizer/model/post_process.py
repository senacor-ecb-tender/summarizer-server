import logging
import nltk
import re
from typing import List


logger = logging.getLogger(__name__)


def process(input_text: str) -> List[str]:
    # split into sentences
    sentences = nltk.sent_tokenize(input_text)
    return list(map(prettify, sentences))


def prettify(sentence: str) -> str:
    return sentence.strip().capitalize().replace('\n', '').replace('  ', ' ') if sentence is not None else None


def download_dict():
    nltk.download('punkt')
