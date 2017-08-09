"""Deterministic topic segmentation.

We split the meeting into topic segments using a transparent, explainable score
rather than an opaque model. A boundary is placed between utterance *i* and
*i+1* when the *cohesion* between their keyword sets drops below a threshold,
optionally reinforced by a long silence gap. Everything here is reproducible:
same input, same segments, every time.
"""

from __future__ import annotations

import re
from collections import Counter
from typing import List, Set

from .model import TopicSegment, Utterance

_WORD_RE = re.compile(r"[a-z0-9']+")

# Common English function words; dropping them focuses cohesion on content.
_STOPWORDS: Set[str] = set(
    """a an and are as at be but by for from had has have he her his i if in into is it
    its me my no not of on or our so that the their them then there these they this to
    up us was we were what when which who will with you your""".split()
)


def _keywords(text: str) -> Counter:
    words = [w for w in _WORD_RE.findall(text.lower()) if w not in _STOPWORDS and len(w) > 2]
    return Counter(words)


def _cohesion(a: Counter, b: Counter) -> float:
