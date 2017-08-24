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
    """Cosine-like overlap of two keyword bags in [0, 1]."""
    if not a or not b:
        return 0.0
    shared = set(a) & set(b)
    if not shared:
        return 0.0
    dot = sum(a[w] * b[w] for w in shared)
    na = sum(v * v for v in a.values()) ** 0.5
    nb = sum(v * v for v in b.values()) ** 0.5
    return dot / (na * nb) if na and nb else 0.0


def segment_topics(
    utterances: List[Utterance],
    cohesion_threshold: float = 0.12,
    silence_gap: float = 8.0,
    window: int = 3,
) -> List[TopicSegment]:
    """Return topic segments covering all utterances.

    - ``cohesion_threshold``: below this, a topic boundary is opened.
    - ``silence_gap``: a pause (seconds) at least this long also opens a boundary.
    - ``window``: how many recent utterances define the "current topic" bag.
    """

    if not utterances:
        return []

    boundaries = [0]
    recent: List[Counter] = [_keywords(utterances[0].text)]
    for i in range(1, len(utterances)):
        cur = _keywords(utterances[i].text)
        context = Counter()
        for c in recent[-window:]:
            context.update(c)
        gap = utterances[i].start - utterances[i - 1].end
        low_cohesion = _cohesion(context, cur) < cohesion_threshold
        big_gap = gap >= silence_gap
        if (low_cohesion and cur) or big_gap:
            boundaries.append(i)
            recent = [cur]
        else:
            recent.append(cur)

    boundaries.append(len(utterances))

    segments: List[TopicSegment] = []
    for seg_id, (lo, hi) in enumerate(zip(boundaries, boundaries[1:])):
        chunk = utterances[lo:hi]
        bag = Counter()
        speakers: List[str] = []
        for u in chunk:
            bag.update(_keywords(u.text))
            if u.speaker not in speakers:
                speakers.append(u.speaker)
        top = [w for w, _ in bag.most_common(5)]
        label = " / ".join(top[:3]) if top else "general discussion"
        segments.append(
            TopicSegment(
                segment_id=seg_id,
