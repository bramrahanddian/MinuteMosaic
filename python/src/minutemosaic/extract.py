"""Explainable extraction of decisions and action items.

The philosophy: no black boxes. Every extracted claim is produced by a named
rule matching a concrete trigger phrase, and carries a Provenance record that
points back to the exact utterance(s) that fired it. Confidence is a bounded,
hand-tuned score derived from *which* signals matched — not a learned opacity.

You can read every rule below and predict the output. That is the point.
"""

from __future__ import annotations

import re
