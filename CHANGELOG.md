# Changelog

All notable changes to MinuteMosaic are documented here. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/). This project is honest about
its scope: it does **not** transcribe audio and has **no** remote service.

## [Unreleased]

### Changed
- Rule wording in `docs/heuristics.md` is being reviewed for the next patch.

## [1.0.0] — 2026-05-19

### Added
- `PrivacySettings.shareSafe` preset: `.days(30)` retention plus transcript
  redaction and speaker pseudonymization in one call.
- Stability commitment for the CLI contract: `segments`, `decisions`, `actions`
  and `report` keep their output shapes across 1.x.

### Changed
- Every extracted claim now carries a human-readable `note` in its provenance,
  explaining any inferred owner/due value.

## [0.9.0] — 2025-06-17

### Added
- `TimelineRenderer` layout of stained-glass facets and self-contained SVG
  export from a report JSON.
- Retention windows (`PrivacySettings.retention`) with pure
  `RetentionEngine.isExpired` checks for background pruning.

## [0.8.0] — 2024-09-17

### Added
- Swift local model (`Meeting`, `Event`, provenance) mirroring the Python world.
- `mm-timeline` executable that reads the Python report JSON and prints or
  exports the evidence timeline.

## [0.7.0] — 2023-11-14

### Added
- Talk-time totals and per-topic speaker listings in the report stats.
- `docs/heuristics.md`: the full rule table with example triggers and base
  confidences, so output stays predictable by reading.

## [0.6.0] — 2022-08-30

### Added
- Self-contained HTML report: inline CSS, no CDN, no fetched fonts, clickable
  evidence links from every decision/action back to its source utterance.

## [0.5.0] — 2021-02-16

### Added
- `Provenance` on every decision and action: `rule_id`, matched `trigger`,
  `utterance_indices` and a note. Confidence clipped to `[0.05, 0.99]`.

## [0.4.0] — 2019-10-08

### Added
- Action extraction with `action.assign`, `action.imperative` and
  `action.followup` rules.
- Owner and due inference with bounded confidence bonuses (`+0.12` owner,
  `+0.10` due).

## [0.3.0] — 2018-06-05

### Added
- Explainable decision extraction: ordered `decide.*` regex rules,
  strongest-first, base confidence per rule.

## [0.2.0] — 2017-03-21

### Added
- Deterministic topic segmentation via keyword cohesion with a silence-gap
  override; each segment labelled from its top keywords.

## [0.1.0] — 2015-07-14

### Added
- JSONL transcript ingestion, stdlib only: forgiving key spellings, line-numbered
  errors, timing preserved verbatim.
- Core data model (`Utterance`, `Segment`, `MeetingReport`) and JSON report
  output.

<!-- draft note 1360 -->
