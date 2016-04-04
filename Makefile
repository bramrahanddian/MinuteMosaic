# minutemosaic — local-first meeting intelligence
# Python is stdlib-only; Swift builds where a toolchain is available.

PYTHON ?= python
EXAMPLE = examples/product-sync.jsonl
OUT_HTML = examples/product-sync.report.html
OUT_JSON = examples/product-sync.report.json
PYSRC = python/src

.PHONY: help
help:
	@echo "Targets:"
	@echo "  make report      - build HTML + JSON report from the example transcript"
	@echo "  make decisions   - print detected decisions with provenance"
	@echo "  make actions     - print detected action items with provenance"
	@echo "  make segments    - print detected topic segments"
	@echo "  make compile-py  - byte-compile all Python sources (syntax check)"
	@echo "  make swift-build  - build the Swift package (needs a Swift toolchain)"
	@echo "  make swift-timeline - render the timeline from the example report JSON"
	@echo "  make clean        - remove generated artifacts"

.PHONY: report
report:
	cd $(PYSRC) && $(PYTHON) -m minutemosaic report ../../$(EXAMPLE) \
		--title "Product Sync" --html ../../$(OUT_HTML) --json ../../$(OUT_JSON)

.PHONY: decisions
decisions:
	cd $(PYSRC) && $(PYTHON) -m minutemosaic decisions ../../$(EXAMPLE)

.PHONY: actions
actions:
	cd $(PYSRC) && $(PYTHON) -m minutemosaic actions ../../$(EXAMPLE)

.PHONY: segments
segments:
	cd $(PYSRC) && $(PYTHON) -m minutemosaic segments ../../$(EXAMPLE)

.PHONY: compile-py
compile-py:
	$(PYTHON) -m compileall -q $(PYSRC)/minutemosaic

.PHONY: swift-build
swift-build:
	swift build

.PHONY: swift-timeline
