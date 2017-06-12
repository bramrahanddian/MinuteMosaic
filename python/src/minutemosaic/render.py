"""Renderers: JSON (machine) and HTML (human, self-contained, offline).

The HTML report is a single file with inline CSS — no CDN, no fonts fetched, no
JavaScript phoning home. It renders a stained-glass evidence timeline where each
derived claim links to its source utterances so a reader can verify provenance
by eye.
"""

from __future__ import annotations

import html
import json
from typing import List

from .model import MeetingReport, Utterance


def render_json(report: MeetingReport, *, indent: int = 2) -> str:
    return json.dumps(report.to_dict(), indent=indent, ensure_ascii=False)


def _fmt_time(seconds: float) -> str:
