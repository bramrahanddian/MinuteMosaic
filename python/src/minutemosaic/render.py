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
    seconds = int(round(seconds))
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def _confidence_class(c: float) -> str:
    if c >= 0.8:
        return "conf-high"
    if c >= 0.6:
        return "conf-med"
    return "conf-low"


_PALETTE = ["#c1272d", "#e8a33d", "#2e7d32", "#1565c0", "#6a1b9a", "#00838f", "#ad1457"]


def _seg_color(seg_id: int) -> str:
    return _PALETTE[seg_id % len(_PALETTE)]


def render_html(report: MeetingReport) -> str:
    d = report.to_dict()
    esc = html.escape

    utter_by_index = {u.index: u for u in report.utterances}

    # Stained-glass timeline: one facet per utterance, tinted by segment.
    span = max(1e-6, report.utterances[-1].end - report.utterances[0].start)
    t0 = report.utterances[0].start
    seg_of = {}
    for s in report.segments:
        for i in range(s.start_index, s.end_index + 1):
            seg_of[i] = s.segment_id

    facets = []
    for u in report.utterances:
