"""Transcript ingestion.

Input format: JSON Lines (JSONL), one utterance object per line. Each object
must carry a speaker, text and timing. We accept a couple of common key
spellings to be forgiving, but we never fabricate missing timing — a line
without usable timestamps is rejected with a clear, line-numbered error.

Example line::

    {"start": 12.4, "end": 15.9, "speaker": "Ada", "text": "Let's ship Friday."}
"""

from __future__ import annotations

import json
from typing import Iterable, List, Tuple

from .model import Utterance


class TranscriptError(ValueError):
    """Raised when a transcript line cannot be parsed into an Utterance."""


_START_KEYS = ("start", "start_time", "ts", "t0", "begin")
_END_KEYS = ("end", "end_time", "t1", "stop")
_SPEAKER_KEYS = ("speaker", "spk", "who", "name")
_TEXT_KEYS = ("text", "content", "utterance", "words")


def _first(obj: dict, keys: Tuple[str, ...]):
    for k in keys:
        if k in obj and obj[k] is not None:
