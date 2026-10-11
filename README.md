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
> `.github/workflows/ci.yml`, `swift build` on macOS). The sources are written to
> that expectation.

---

## 🧩 How a claim becomes a pane

```
   transcript line ──▶ heuristic rule ──▶ claim ──▶ provenance
        #3                decide.agree      Decision   rule=decide.agree
   "Let's go with…"       "Let's go with"   conf 0.77  trigger='Let's go with'
                                                       evidence=[#3]
        ▲                                                   │
        └───────────────── audit trail ─────────────────────┘
```

You can walk it forwards (line → claim) or backwards (claim → line). Both
directions are always available because provenance is a first-class field, not
an afterthought. Read the full rule table in
[`docs/heuristics.md`](docs/heuristics.md).

---

## 📐 Design principles

1. **Provenance or it didn't happen.** A claim with no source spans is a bug.
2. **Deterministic.** Same transcript in → same mosaic out, every run.
3. **Readable rules.** If you can't predict the output by reading the code, the
   rule is too clever.
4. **Local-first, always.** No network, no accounts, no telemetry.
5. **Honest scope.** No audio processing. No fabricated timestamps. No claims of
   certainty the heuristics can't justify (confidence is clipped to 0.05–0.99).

---

## 📁 Layout

```
minutemosaic/
├── python/src/minutemosaic/     # stdlib-only CLI + library
│   ├── ingest.py                #   JSONL → Utterances (forgiving, strict on timing)
│   ├── segment.py               #   deterministic topic boundaries
│   ├── extract.py               #   explainable decision/action rules + provenance
│   ├── report.py                #   assemble MeetingReport
│   ├── render.py                #   self-contained HTML + JSON
│   └── cli.py                   #   `minutemosaic` command
├── Sources/
│   ├── MinuteMosaic/            # Swift local model, privacy, timeline renderer
│   └── mm-timeline/             # Swift executable
├── examples/product-sync.jsonl  # a short, hand-authored meeting
├── docs/                        # heuristics, transcript format, animated SVGs
├── Package.swift · pyproject.toml · Makefile
├── .github/workflows/ci.yml     # Python compile+smoke, Swift build
├── ROADMAP.md · CHANGELOG.md · LICENSE
```

---

## 📊 Transcript format (the raw light)

One JSON object per line. Times in seconds from start. Full spec in
[`docs/transcript-format.md`](docs/transcript-format.md).

```json
{"start": 0.0, "end": 4.2, "speaker": "Ada",  "text": "Let's start with the release timeline."}
{"start": 4.5, "end": 9.1, "speaker": "Ravi", "text": "Build is green but onboarding has two blocking bugs."}
```

---

## 🗺️ Status

Four milestones are honestly **done** — ingestion, explainable structure,
provenance + reports, and the local Swift model with privacy/export. Things that
are deliberately **not** built (transcription, cloud sync, ML models, automated
tests) are listed just as plainly in [`ROADMAP.md`](ROADMAP.md). We would rather
under-promise the glass than paint light that isn't there.

---

## 📜 License

MIT — see [`LICENSE`](LICENSE). Assemble your own windows.

---

## 🔍 A worked example: following the lead

Take utterance `#8` from the bundled transcript:

```json
{"start": 51.3, "end": 55.8, "speaker": "Mei", "text": "Sure, I'll send the mockups to marketing by Thursday."}
```

Here is exactly what MinuteMosaic does with it, step by step, all reproducible:

1. **Ingest** assigns it `index = 8`, keeps its timing verbatim (`51.3 → 55.8`),
   and records the speaker `Mei`. Nothing is guessed.
2. **Segment** places it in a topic whose keywords are `send / mockups /
   marketing` — the pricing-copy thread, not onboarding.
3. **Extract** runs the action rules top-down. `action.assign` matches the
   phrase `mockups to marketing by Thursday.`
4. **Owner inference** sees `I'll` and attributes the action to the current
   speaker, `Mei` (bonus `+0.12`).
5. **Due inference** sees `by Thursday` and captures `Thursday` (bonus `+0.10`).
6. **Confidence** = clip(0.70 base + 0.12 + 0.10) = **0.92**.
7. **Provenance** is stamped: `rule=action.assign`,
   `trigger='mockups to marketing by Thursday.'`, `utterance_indices=[8]`,
   with a note recording the inferred owner and due.

The JSON report carries all of that so any downstream tool — including the Swift
`mm-timeline` — can re-verify the claim against the source. No pane floats free.

---

## 🔐 Privacy & retention (Swift side)

Because everything is local, *you* decide what leaves your machine — and even
then only when you deliberately export.

| Setting | Default | Effect |
|---------|---------|--------|
| `retention` | `.forever` | `.days(N)` marks older meetings expired for pruning |
| `redactTranscriptOnExport` | `false` | replaces text with a length-preserving `•` mask so the *shape* survives, the *content* does not |
| `pseudonymizeSpeakers` | `false` | remaps real names to stable `Speaker A/B/…` aliases |

A ready-made preset ships for the common "share the shape, not the words" case:

```swift
let settings = PrivacySettings.shareSafe   // .days(30) + redact + pseudonymize
let json = try TimelineRenderer.exportJSON(meeting, settings: settings)
```

`RetentionEngine.isExpired(recordedAt:settings:now:)` is a pure function you can
call from a background prune task. There is no hidden retention — if a meeting is
on disk, it is because your policy kept it there.

---

## ❓ FAQ

**Does this transcribe my audio / join my meeting?**
No. It never touches audio and never joins anything. You feed it a transcript
that already exists. The waveform artwork represents a transcript's rhythm.

**Does it call an LLM or any API?**
No. Python is stdlib-only with zero runtime dependencies. Swift makes no network
calls. Run it on a plane.

**Why heuristics instead of a model?**
So you can audit every claim. A regex you can read beats a probability you can't.
When we say confidence `0.92`, the [`docs/heuristics.md`](docs/heuristics.md)
table tells you precisely why.

**Can it be wrong?**
Yes — heuristics miss and over-fire. That is exactly why every claim ships its
source spans: the report is designed for a human to verify in seconds, not to be
trusted blindly.

**What about other languages / accents?**
The rules are English-oriented today. Because they are just readable patterns,
adding a language means adding patterns — no retraining, no data collection.

**Where are the tests?**
There are none yet, and the ROADMAP says so honestly. The code is verified
manually against the bundled example and byte-compiled in CI. The bundled
example doubles as the smoke fixture: every CI run replays it through
`segments`, `decisions`, `actions` and `report`.

---

## 🛠️ Contributing a new rule

1. Add a `(rule_id, compiled_regex, base_confidence)` tuple to `_DECISION_RULES`
   or `_ACTION_RULES` in `python/src/minutemosaic/extract.py`.
2. Keep it readable — if a teammate can't predict when it fires, simplify it.
3. Document it in the table in `docs/heuristics.md`.
4. Run `make decisions` / `make actions` against the example and confirm the
   provenance line shows your `rule_id` and trigger.

That's the whole loop. New glass, same lead.

<div align="center">
<sub>MinuteMosaic · leaded glass for meetings · every pane traceable to the light that made it</sub>
</div>
