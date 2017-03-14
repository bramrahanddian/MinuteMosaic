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

