import json
import pathlib
from collections import deque
from typing import List, Generator

import faiss
import nltk
import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer

from ..utils.tracing import traced

PATH = pathlib.Path(__file__).parent

with open(PATH / "topics.json", "rt") as f:
    TOPICS = json.load(f)
    assert len(TOPICS) == 4

with open(PATH / "keywords.json", "rt") as f:
    KEYWORDS = json.load(f)
    assert len(KEYWORDS) == 4

TOPIC_VECTORS = np.loadtxt(str(PATH / "topic-vectors.txt"))
assert len(TOPICS) == TOPIC_VECTORS.shape[0]

vectorizer = HashingVectorizer(n_features=TOPIC_VECTORS.shape[1], stop_words='english')


def windows(sentences: List[str], window_size: int) -> Generator[List[str], None, None]:
    """Iterate over `sentences` in windows of size `window_size`.

    This implementation is borrowed from `more_itertools`.
    """
    window = deque(maxlen=window_size)
    i = window_size
    for _ in map(window.append, sentences):
        i -= 1
        if not i:
            i = 1
            yield list(window)


@traced
def filter_topic(text: str, topic: str, window_size: int = 5,
                 min_sentences: int = 10, fraction_to_keep: float = .25) -> str:
    """Extract sentences from the `text´ that match the `topic`.

    :param text: The text to filter.
    :param topic: The topic to extract from the text. Must be one of the pre-defined topics.
    :param window_size: The size of the sliding window. See `func:.windows`.
    :param min_sentences: The minimum number of sentences to return.
    :param fraction_to_keep: Fraction of windows to keep. If the resulting number of sentences is lower
                             than the specified `min_sentences`, another `fraction_to_keep` windows is added
                             until that threshold is reached.
    :return:
    """
    try:
        topic_idx = TOPICS.index(topic)
    except ValueError:
        raise ValueError(f"Unknown topic {topic}. Known topics: {TOPICS}.")

    sentences = nltk.sent_tokenize(text.strip())

    if len(sentences) <= min_sentences:
        return text

    sentences_to_keep = _extract_similar_sentences(sentences=sentences,
                                                   topic_idx=topic_idx,
                                                   window_size=window_size,
                                                   min_sentences=min_sentences,
                                                   fraction_to_keep=fraction_to_keep)

    sentences_to_keep += _extract_sentences_with_keywords(sentences, KEYWORDS[topic])
    sentences_to_keep = sorted(list(set(sentences_to_keep)))

    return " ".join((sentences[sentence_idx] for sentence_idx in sentences_to_keep))


def _extract_similar_sentences(sentences: List[str],
                               topic_idx: int,
                               window_size: int,
                               min_sentences: int,
                               fraction_to_keep: float) -> List[int]:
    windowed = [" ".join(win) for win in windows(sentences, window_size)]
    hashed = vectorizer.transform(windowed).toarray().astype(np.float32)

    index = faiss.IndexFlatIP(TOPIC_VECTORS.shape[1])
    index.add(hashed)

    k = len(sentences)
    _, window_indices = index.search(TOPIC_VECTORS.astype(np.float32), k)

    topic_indices = list(window_indices[topic_idx])

    sentences_to_keep = []
    start_idx = 0
    while len(sentences_to_keep) <= min_sentences:
        windows_to_keep = sorted(topic_indices[start_idx:int(k * fraction_to_keep + 1)])
        sentences_to_keep.extend(set((window_idx + i for i in range(window_size)
                                      for window_idx in windows_to_keep)))

    return sentences_to_keep


def _extract_sentences_with_keywords(sentences: List[str], keywords: List[str]) -> List[int]:
    return [i for i, sentence in enumerate(sentences)
            if any(filter(lambda x: x in sentence.lower() or x in sentence, keywords))]
