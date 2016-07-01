<!-- ┌───────────────────────────────────────────────────────────────────────┐ -->
<!-- │  M i n u t e M o s a i c  ·  every claim is a pane of stained glass     │ -->
<!-- └───────────────────────────────────────────────────────────────────────┘ -->

<div align="center">

# 🪟 MinuteMosaic

### *Meeting intelligence assembled like stained glass — every pane a claim, every claim leaded to its source.*

<img src="docs/assets/timeline.svg" alt="Animated stained-glass evidence timeline" width="100%">

**Local-first · offline · stdlib-only Python · Swift for the timeline · no audio, no cloud, no magic**

</div>

---

```
    ░░░░░░  ▓▓▓▓▓▓▓▓▓▓  ██████  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▒▒▒▒▒  ▓▓▓▓▓▓▓▓  ████████  ▒▒▒▒
    │      │           │       │               │      │         │         │
    0:00   onboarding  RC cut  pricing redesign  copy  incident  alerting  end
     ◂──────────────────────  playhead sweeps the meeting  ──────────────────▸
```

Think of a meeting transcript as light. Raw, it floods the room without shape.
**MinuteMosaic** cuts that light into panes — topics, decisions, action items —
and *leads* each pane with the one thing most meeting tools throw away: **where
it came from.** Click any decision and you land on the exact utterance that said
it. No summary you have to take on faith.

> **Honesty first.** MinuteMosaic does **not** transcribe audio and has **no**
> remote service. It consumes a transcript you already have and derives structure
> with rules you can read in an afternoon. The waveform in the diagrams is the
> *rhythm of a transcript*, not a claim that we run speech recognition.

---

## 🎨 The mosaic, pane by pane

| Pane | What it is | Where the glass comes from |
|------|-----------|----------------------------|
| 🟥 **Ingest** | JSONL transcript loader (stdlib) | forgiving key spellings, line-numbered errors, never fabricates timing |
| 🟧 **Segment** | Deterministic topic boundaries | keyword cohesion + silence gaps |
| 🟩 **Decide** | Explainable decision extraction | ordered regex rules, bounded confidence |
| 🟦 **Act** | Action items with owner/due inference | pattern-matched, honestly scored |
| 🟪 **Provenance** | The lead between every pane | rule id + trigger phrase + source spans |
| 🟦 **Report** | Self-contained HTML + JSON | offline, no CDN, clickable evidence |
| 🟥 **Swift timeline** | Local model, privacy, SVG export | retention windows, redaction, pseudonymization |

<img src="docs/assets/provenance.svg" alt="Animated provenance pipeline" width="100%">

---

## 🔊 Why "audio timeline" if there's no audio?

Because the *timeline* is the instrument, not the microphone. A meeting has a
rhythm — bursts of debate, long silences, a single decisive sentence. MinuteMosaic
lays that rhythm out horizontally like an audio scrubber and tints each utterance
by its topic, so the **shape** of the conversation is visible at a glance:

```
   loud debate        silence          one clean decision           follow-ups
   ▁▂▅▇█▇▅▂▁▂▅▇▂▁      ·  ·  ·  ·       ▁▂▃  ██  ▃▂▁                 ▂▄▂▄▂▄▂
   └── topic: onboarding ──┘           └ "let's go with Friday" ┘   └ actions ┘
```

The stained-glass panes above the scrubber are the **evidence facets** — one per
utterance. Hover a facet in the HTML report and you see the raw line; the derived
claims below link straight back to it.

---

## 🚀 Quickstart (Python, stdlib only)

No dependencies. No virtualenv required. Just Python 3.9+.

```bash
cd python/src

# See the topic mosaic
python -m minutemosaic segments  ../../examples/product-sync.jsonl

# Decisions, each with its provenance
python -m minutemosaic decisions ../../examples/product-sync.jsonl

# Action items with inferred owner / due
python -m minutemosaic actions   ../../examples/product-sync.jsonl

# Build the full stained-glass report (HTML + JSON)
python -m minutemosaic report ../../examples/product-sync.jsonl \
    --title "Product Sync" \
    --html ../../examples/product-sync.report.html \
    --json ../../examples/product-sync.report.json
```

Or from the project root with the Makefile:

```bash
make segments
make decisions
make actions
make report        # writes examples/product-sync.report.{html,json}
make compile-py    # byte-compile every source (syntax check)
```

### What the decisions command prints

```
D0 (0.77) Ada: Great. Let's go with a Friday cutoff for the release candidate then.
    rule=decide.agree trigger='Let's go with' evidence=#3
D2 (0.95) Mei: We decided last sprint to go with the three-tier layout, so I'll finalize the copy.
    rule=decide.explicit trigger='We decided' evidence=#6
```

Every line tells you **which rule fired**, **on what phrase**, and **which source
utterance** backs it. That's the lead holding the glass.

---

## 🍎 Swift: the local evidence timeline

The Swift package (`Package.swift`, `Sources/MinuteMosaic`) is a **local model**
of the same world — transcript, events, provenance — plus:

- **`PrivacySettings` / `RetentionEngine`** — keep meetings forever or for *N*
  days; on export, optionally redact transcript text (length-preserving mask)
  and pseudonymize speakers.
- **`TimelineRenderer`** — lay out stained-glass facets, render the evidence
  timeline as text, and export a self-contained **SVG** — all with zero UI
  framework so it builds headless in CI.
- **`mm-timeline`** — a tiny executable that reads the Python report JSON and
  prints/exports the timeline.

```bash
# Requires a Swift toolchain (CI builds this on macOS)
swift build
swift run mm-timeline examples/product-sync.report.json --svg examples/timeline.export.svg
swift run mm-timeline examples/product-sync.report.json --share-safe   # redacted + pseudonymized
```

> **Local build note:** this project's Python side was compiled and run locally
> against the bundled example. A Swift toolchain was **not** available in the
> authoring environment, so the Swift package is compiled by **CI** (see
