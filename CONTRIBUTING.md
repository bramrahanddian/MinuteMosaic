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
