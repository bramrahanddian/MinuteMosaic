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
