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
