# minutemosaic — local-first meeting intelligence
# Python is stdlib-only; Swift builds where a toolchain is available.

PYTHON ?= python
EXAMPLE = examples/product-sync.jsonl
OUT_HTML = examples/product-sync.report.html
OUT_JSON = examples/product-sync.report.json
PYSRC = python/src

.PHONY: help
help:
