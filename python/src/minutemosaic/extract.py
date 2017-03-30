"""Explainable extraction of decisions and action items.

The philosophy: no black boxes. Every extracted claim is produced by a named
rule matching a concrete trigger phrase, and carries a Provenance record that
points back to the exact utterance(s) that fired it. Confidence is a bounded,
hand-tuned score derived from *which* signals matched — not a learned opacity.

You can read every rule below and predict the output. That is the point.
"""

from __future__ import annotations

import re
from typing import List, Optional

from .model import ActionItem, Decision, Provenance, Utterance

# --- Decision triggers -----------------------------------------------------
# Ordered strongest-first. Each entry: (rule_id, compiled regex, base_confidence)
_DECISION_RULES = [
    ("decide.explicit", re.compile(r"\b(we (?:have )?decided|decision is|it's decided|we'll go with|we will go with)\b", re.I), 0.9),
    ("decide.agree", re.compile(r"\b(let's|lets|we should|we'll|we will)\s+(go with|ship|adopt|use|pick|choose|proceed with)\b", re.I), 0.72),
    ("decide.consensus", re.compile(r"\b(agreed|sounds good|works for me|approved|sign(?:ed)? off|greenlight)\b", re.I), 0.6),
    ("decide.final", re.compile(r"\b(final(?:ized|ised)?|locked in|settled)\b", re.I), 0.55),
]

# --- Action triggers -------------------------------------------------------
_ACTION_RULES = [
    ("action.assign", re.compile(r"\b(\w+) (?:will|to|is going to|'ll)\s+(\w+[\w\s]{2,40}?)(?:\bby\b|[.?!]|$)", re.I), 0.7),
    ("action.imperative", re.compile(r"\b(please |can you |could you |let's |we need to |need to |todo:?\s*)\b", re.I), 0.62),
    ("action.followup", re.compile(r"\b(follow up|follow-up|action item|take that offline|circle back|send (?:the|an|a)?)\b", re.I), 0.58),
]

_OWNER_RE = re.compile(r"\b([A-Z][a-z]+)\s+(?:will|to|is going to|'ll|should|can)\b")
_DUE_RE = re.compile(
    r"\bby\s+(next week|end of (?:day|week|month)|eod|eow|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday|[A-Z][a-z]+ \d{1,2}|\d{1,2}(?:st|nd|rd|th)?)\b",
    re.I,
)


