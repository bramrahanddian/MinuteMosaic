"""minutemosaic — local-first meeting intelligence with evidence provenance.

This package is deliberately stdlib-only. It performs *no* audio processing and
makes *no* transcription claims: it consumes an already-produced timestamped
speaker transcript (JSONL) and derives structure (topics, decisions, action
items) using deterministic, explainable heuristics. Every derived claim carries
a provenance trail back to the exact source spans that triggered it.
"""

__version__ = "0.4.0"

__all__ = ["__version__"]
