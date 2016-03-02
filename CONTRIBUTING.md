# Contributing to MinuteMosaic

Thanks for considering a contribution. MinuteMosaic is local-first and honest
about its scope: it does not transcribe audio and never calls a remote service.
It reads an existing timestamped transcript and derives structure with rules a
reader can audit.

## Development setup

- **Python 3.9+** — the CLI and library are stdlib-only; there is nothing to
  install and no virtualenv is required.

```bash
python -m compileall -q python/src/minutemosaic
cd python/src
python -m minutemosaic segments  ../../examples/product-sync.jsonl
python -m minutemosaic decisions ../../examples/product-sync.jsonl
python -m minutemosaic actions   ../../examples/product-sync.jsonl
python -m minutemosaic report ../../examples/product-sync.jsonl \
    --title "Product Sync" --html /tmp/report.html --json /tmp/report.json
```

- **Swift (optional)** — the local timeline model builds where a toolchain is
  available: `swift build` and `swift run mm-timeline <report.json>`.

## Before you open a pull request

1. `python -m compileall -q python/src/minutemosaic` passes.
2. The CLI runs clean against `examples/product-sync.jsonl`.
3. Every new extraction rule is readable, documented in the rule table in
   `docs/heuristics.md`, and keeps provenance (rule id + trigger + source spans).
4. Keep the Python package dependency-free and offline.
