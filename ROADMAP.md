# MinuteMosaic roadmap

The four checked milestones are shipped. The project intentionally makes no transcription or cloud claims.

## Completed foundation
- [x] **M1 — Faithful transcript ingestion.** JSONL loader preserves timing and reports line-numbered errors.
- [x] **M2 — Explainable structure.** Deterministic topic segmentation and rule-based decision/action extraction.
- [x] **M3 — Evidence-linked reports.** Every claim points to source utterances in offline HTML and JSON.
- [x] **M4 — Swift local model.** Privacy settings, retention/redaction controls, timeline model, and text/SVG export.

## Planned / explicitly not implemented
- [ ] Optional, isolated local ASR integration.
- [ ] Automated test suites.
- [ ] A `--summary` mode that prints counts only, for dashboards and CI logs.
- [ ] Additional export formats.

## Permanent constraints
- No cloud accounts or mandatory synchronization.
- No fabricated audio/transcription capabilities; current input is an existing transcript.
