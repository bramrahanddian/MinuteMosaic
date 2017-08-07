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
