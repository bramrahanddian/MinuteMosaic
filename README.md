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
