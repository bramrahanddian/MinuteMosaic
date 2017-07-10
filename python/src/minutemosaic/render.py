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

    transcript_html = []
    for u in report.utterances:
        color = _seg_color(seg_of.get(u.index, 0))
        transcript_html.append(
            f'<div class="utt" id="u{u.index}">'
            f'<span class="ubar" style="background:{color}"></span>'
            f'<span class="ut">{_fmt_time(u.start)}</span>'
            f'<span class="us">{esc(u.speaker)}</span>'
            f'<span class="ux">{esc(u.text)}</span></div>'
        )

    stats = d["stats"]
    talk = "".join(
        f"<li>{esc(spk)}: {secs:.0f}s</li>"
        for spk, secs in sorted(stats["talk_time_seconds"].items(), key=lambda kv: -kv[1])
    )

    return _TEMPLATE.format(
        title=esc(report.title),
        generated=esc(report.generated_at),
        source=esc(report.source),
        facets="".join(facets),
        seg_rows="".join(seg_rows),
        decisions=decision_html,
        actions=action_html,
        transcript="".join(transcript_html),
        u_count=stats["utterance_count"],
        s_count=stats["segment_count"],
        d_count=stats["decision_count"],
        a_count=stats["action_count"],
        talk=talk,
        span=_fmt_time(stats["meeting_span_seconds"]),
    )


_TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — minutemosaic</title>
<style>
:root {{ --bg:#0f1013; --panel:#17181d; --ink:#e9e7df; --muted:#9a978d; --line:#2a2b31; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink);
  font:15px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif; }}
header {{ padding:28px 24px; border-bottom:1px solid var(--line);
  background:linear-gradient(120deg,#1b1c22,#101116); }}
h1 {{ margin:0 0 4px; font-size:26px; letter-spacing:.3px; }}
.sub {{ color:var(--muted); font-size:13px; }}
.wrap {{ max-width:960px; margin:0 auto; padding:24px; }}
.timeline {{ position:relative; height:64px; border-radius:8px; overflow:hidden;
  background:#0a0a0c; border:1px solid var(--line); box-shadow:inset 0 0 24px #000; }}
.facet {{ position:absolute; top:0; height:100%; opacity:.82; border-right:1px solid #0a0a0c;
  transition:opacity .15s; }}
.facet:hover {{ opacity:1; }}
.grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin:18px 0; }}
.stat {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:14px; }}
.stat b {{ display:block; font-size:24px; }}
.stat span {{ color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.5px; }}
h2 {{ margin:28px 0 12px; font-size:18px; border-left:3px solid #e8a33d; padding-left:10px; }}
ul.seg {{ list-style:none; padding:0; margin:0; }}
ul.seg li {{ padding:6px 0; border-bottom:1px solid var(--line); }}
.chip {{ display:inline-block; width:12px; height:12px; border-radius:3px; margin-right:8px;
  vertical-align:middle; }}
.muted {{ color:var(--muted); }}
.claim {{ background:var(--panel); border:1px solid var(--line); border-left-width:4px;
  border-radius:8px; padding:14px; margin:12px 0; }}
.conf-high {{ border-left-color:#2e7d32; }}
.conf-med {{ border-left-color:#e8a33d; }}
.conf-low {{ border-left-color:#c1272d; }}
.claim-head {{ display:flex; justify-content:space-between; align-items:center; }}
.badge {{ font-size:11px; text-transform:uppercase; letter-spacing:.6px; color:#0f1013;
  background:#e9e7df; padding:2px 8px; border-radius:20px; }}
.conf {{ color:var(--muted); font-size:12px; }}
.claim-text {{ margin:8px 0 4px; font-size:15px; }}
.meta {{ margin:0; color:var(--muted); font-size:13px; }}
.prov {{ margin:8px 0 2px; font-size:12px; color:#b9c6e0; }}
.prov-note {{ margin:0; font-size:12px; color:var(--muted); font-style:italic; }}
code {{ background:#0a0a0c; padding:1px 5px; border-radius:4px; color:#e8a33d; }}
a.ev {{ color:#7fb0ff; text-decoration:none; border-bottom:1px dotted #7fb0ff; }}
.utt {{ display:flex; gap:10px; padding:6px 0; align-items:baseline;
  border-bottom:1px solid #202127; }}
