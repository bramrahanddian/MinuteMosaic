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
        left = (u.start - t0) / span * 100.0
        width = max(0.4, u.duration / span * 100.0)
        color = _seg_color(seg_of.get(u.index, 0))
        title = esc(f"[{_fmt_time(u.start)}] {u.speaker}: {u.text}")
        facets.append(
            f'<span class="facet" style="left:{left:.3f}%;width:{width:.3f}%;'
            f'background:{color}" title="{title}" data-idx="{u.index}"></span>'
        )

    seg_rows = []
    for s in report.segments:
        seg_rows.append(
            f'<li><span class="chip" style="background:{_seg_color(s.segment_id)}"></span>'
            f'<strong>{esc(s.label)}</strong> '
            f'<span class="muted">{_fmt_time(s.start_time)}–{_fmt_time(s.end_time)} · '
            f'{esc(", ".join(s.speakers))}</span></li>'
        )

    def claim_block(kind: str, cid: int, text: str, meta: str, conf: float, prov) -> str:
        links = " ".join(
            f'<a href="#u{i}" class="ev">#{i}</a>' for i in prov.utterance_indices
        )
        return (
            f'<div class="claim {_confidence_class(conf)}">'
            f'<div class="claim-head"><span class="badge">{kind} {cid}</span>'
            f'<span class="conf">confidence {conf:.2f}</span></div>'
            f'<p class="claim-text">{esc(text)}</p>'
            f'<p class="meta">{esc(meta)}</p>'
            f'<p class="prov">rule <code>{esc(prov.rule_id)}</code> · '
            f'trigger <code>{esc(prov.trigger.strip())}</code> · evidence {links}</p>'
            f'<p class="prov-note">{esc(prov.note)}</p>'
            f"</div>"
        )

    decision_html = "".join(
        claim_block(
            "Decision",
            dec.decision_id,
            dec.text,
            f"{dec.speaker} @ {_fmt_time(dec.time)}",
            dec.confidence,
            dec.provenance,
        )
        for dec in report.decisions
    ) or '<p class="muted">No decisions detected.</p>'

    action_html = "".join(
        claim_block(
            "Action",
            act.action_id,
            act.text,
            f"owner: {act.owner or 'unassigned'} · due: {act.due_hint or 'n/a'} · "
            f"{act.speaker} @ {_fmt_time(act.time)}",
            act.confidence,
            act.provenance,
        )
        for act in report.actions
    ) or '<p class="muted">No action items detected.</p>'
