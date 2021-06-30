import pathlib
import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer
import nltk.data
import itertools
from collections import deque
from typing import List, Generator
import faiss


PATH = pathlib.Path(__file__).parent

TOPICS = ["crazy", "topic"]
TOPIC_VECTORS = np.random.rand(2, 16)
assert len(TOPICS) == TOPIC_VECTORS.shape[0]

sentence_detector = nltk.data.load("tokenizers/punkt/english.pickle")

vectorizer = HashingVectorizer(TOPIC_VECTORS.shape[1])


def windows(sentences: List[str], window_size: int) -> Generator[List[str], None, None]:
    """This implementation is borrowed from `more_itertools`."""
    window = deque(maxlen=window_size)
    i = window_size
    for _ in map(window.append, sentences):
        i -= 1
        if not i:
            i = 1
            yield list(window)


def filter_topic(text: str, topic: str, window_size: int = 3) -> str:
    try:
        topic_idx = TOPICS.index(topic)
    except ValueError:
        raise ValueError(f"Unknown topic {topic}. Known topics: {TOPICS}.")

    sentences = sentence_detector.tokenize(text.strip())
    windowed = [" ".join(win) for win in windows(sentences, window_size)]
    hashed = vectorizer.transform(windowed)

    index = faiss.IndexFlatIP(TOPIC_VECTORS.shape[1])
    index.add(hashed)

    k = len(sentences)
    similarities, window_indices = index.search(TOPIC_VECTORS.astype(np.float32), k)

    topic_similarities = list(similarities[topic_idx])
    topic_indices = list(window_indices[topic_idx])

    # TODO: Filter by confidence

    windows_to_keep = sorted(topic_indices[:int(k/2 + 1)])
    sentences_to_keep = set((window_idx + i for i in range(window_size) for window_idx in windows_to_keep))

    return " ".join((sentences[sentence_idx] for sentence_idx in sentences_to_keep))


if __name__ == "__main__":
    filter_topic("hello there. I'm a sentence about Mr. Smith. There are more. And more. But too few.", "crazy")
