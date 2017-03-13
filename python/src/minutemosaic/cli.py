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

