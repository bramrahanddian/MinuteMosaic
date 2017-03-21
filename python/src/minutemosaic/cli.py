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


