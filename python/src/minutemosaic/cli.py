"""Command-line interface for minutemosaic.

Stdlib-only. Usage::

    python -m minutemosaic report transcript.jsonl --html out.html --json out.json
    python -m minutemosaic segments transcript.jsonl
    python -m minutemosaic decisions transcript.jsonl

The tool never touches audio and never claims to transcribe. It consumes an
existing timestamped speaker transcript and derives structure with explainable
heuristics, keeping full provenance.
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from . import __version__
from .ingest import TranscriptError, load_file
from .render import render_html, render_json
from .report import build_report


def _add_common(p: argparse.ArgumentParser) -> None:
    p.add_argument("transcript", help="path to a timestamped speaker transcript (JSONL)")
    p.add_argument("--title", default="Meeting", help="report title")
    p.add_argument(
        "--cohesion",
        type=float,
        default=0.12,
        help="topic cohesion threshold; lower = fewer, broader topics",
    )
    p.add_argument(
        "--silence-gap",
        type=float,
        default=8.0,
        help="silence (seconds) that forces a topic boundary",
    )


def _build(args) -> "object":
    utterances = load_file(args.transcript)
    return build_report(
        utterances,
        title=args.title,
        source=args.transcript,
        cohesion_threshold=args.cohesion,
        silence_gap=args.silence_gap,
    )


def _cmd_report(args) -> int:
    report = _build(args)
    wrote = False
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            fh.write(render_json(report))
        print(f"wrote JSON report  -> {args.json}")
        wrote = True
    if args.html:
        with open(args.html, "w", encoding="utf-8") as fh:
            fh.write(render_html(report))
        print(f"wrote HTML report  -> {args.html}")
        wrote = True
    if not wrote:
        # Default: JSON to stdout.
        print(render_json(report))
    return 0


def _cmd_segments(args) -> int:
    report = _build(args)
    for s in report.segments:
        print(
            f"[{s.segment_id}] {s.start_time:6.1f}-{s.end_time:6.1f}  "
            f"{s.label}  ({', '.join(s.speakers)})"
        )
    return 0


def _cmd_decisions(args) -> int:
    report = _build(args)
    if not report.decisions:
        print("(no decisions detected)")
    for dec in report.decisions:
        ev = ",".join(f"#{i}" for i in dec.provenance.utterance_indices)
        print(f"D{dec.decision_id} ({dec.confidence:.2f}) {dec.speaker}: {dec.text}")
        print(f"    rule={dec.provenance.rule_id} trigger='{dec.provenance.trigger.strip()}' evidence={ev}")
    return 0


def _cmd_actions(args) -> int:
    report = _build(args)
    if not report.actions:
        print("(no action items detected)")
    for act in report.actions:
        ev = ",".join(f"#{i}" for i in act.provenance.utterance_indices)
        print(
            f"A{act.action_id} ({act.confidence:.2f}) owner={act.owner or '-'} "
            f"due={act.due_hint or '-'}: {act.text}"
        )
        print(f"    rule={act.provenance.rule_id} trigger='{act.provenance.trigger.strip()}' evidence={ev}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="minutemosaic",
        description="Local-first meeting intelligence with evidence provenance (stdlib only).",
    )
    parser.add_argument("--version", action="version", version=f"minutemosaic {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_report = sub.add_parser("report", help="build a full report (JSON and/or HTML)")
    _add_common(p_report)
    p_report.add_argument("--html", help="write a self-contained HTML report to this path")
    p_report.add_argument("--json", help="write a JSON report to this path")
    p_report.set_defaults(func=_cmd_report)

    p_seg = sub.add_parser("segments", help="print detected topic segments")
    _add_common(p_seg)
    p_seg.set_defaults(func=_cmd_segments)

    p_dec = sub.add_parser("decisions", help="print detected decisions with provenance")
    _add_common(p_dec)
    p_dec.set_defaults(func=_cmd_decisions)

    p_act = sub.add_parser("actions", help="print detected action items with provenance")
    _add_common(p_act)
    p_act.set_defaults(func=_cmd_actions)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except TranscriptError as exc:
        print(f"transcript error: {exc}", file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(f"file not found: {exc.filename}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

# draft note 1443
