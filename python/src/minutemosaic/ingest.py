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
            return obj[k]
    return None


def _coerce_time(value, line_no: int, field: str) -> float:
    if isinstance(value, bool):  # bool is an int subclass; reject explicitly
        raise TranscriptError(f"line {line_no}: {field} must be a number, got bool")
    try:
        return float(value)
    except (TypeError, ValueError):
        raise TranscriptError(
            f"line {line_no}: {field} must be a number, got {value!r}"
        )


def parse_lines(lines: Iterable[str]) -> List[Utterance]:
    """Parse an iterable of raw JSONL strings into ordered Utterances.

    Blank lines and lines beginning with ``#`` (comments) are skipped so hand
    authored fixtures stay readable. Indices are assigned in file order.
    """

    utterances: List[Utterance] = []
    index = 0
    for line_no, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        try:
            obj = json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise TranscriptError(f"line {line_no}: invalid JSON ({exc.msg})") from exc
        if not isinstance(obj, dict):
            raise TranscriptError(f"line {line_no}: expected a JSON object")

        start_raw = _first(obj, _START_KEYS)
        if start_raw is None:
            raise TranscriptError(f"line {line_no}: missing start time")
        start = _coerce_time(start_raw, line_no, "start")

        end_raw = _first(obj, _END_KEYS)
        end = _coerce_time(end_raw, line_no, "end") if end_raw is not None else start

        speaker = _first(obj, _SPEAKER_KEYS) or "UNKNOWN"
        text = _first(obj, _TEXT_KEYS)
        if isinstance(text, list):  # some tools emit word arrays
            text = " ".join(str(w) for w in text)
        if text is None:
            raise TranscriptError(f"line {line_no}: missing text")

        utterances.append(
            Utterance(
                index=index,
                start=start,
                end=max(start, end),
