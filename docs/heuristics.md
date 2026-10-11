# Heuristics & provenance

The whole point of minutemosaic is that you can **read every rule** and predict
its output. There is no learned model and no hidden state.

## Topic segmentation

Boundaries between topics are opened when either:

1. **Cohesion drops.** We build a keyword bag (content words, stopwords removed)
   for a sliding window of recent utterances and compare it to the next
   utterance with a cosine-like overlap. Below `--cohesion` (default `0.12`), a
   boundary opens.
2. **A long silence occurs.** A gap of at least `--silence-gap` seconds
   (default `8.0`) forces a boundary.

Each segment gets a label from its top keywords.

## Decision extraction

Ordered, strongest-first regex rules (see `extract.py`):

| rule id             | example trigger              | base confidence |
|---------------------|------------------------------|-----------------|
| `decide.explicit`   | "we decided", "decision is"  | 0.90            |
| `decide.agree`      | "let's go with", "we'll ship"| 0.72            |
| `decide.consensus`  | "agreed", "sounds good"      | 0.60            |
| `decide.final`      | "finalized", "locked in"     | 0.55            |

The first rule that matches an utterance wins. Small bonuses apply for complete
sentences.

## Action extraction

| rule id             | example trigger                | base confidence |
|---------------------|--------------------------------|-----------------|
| `action.assign`     | "Mei will finalize the copy"   | 0.70            |
| `action.imperative` | "please", "we need to", "todo:"| 0.62            |
| `action.followup`   | "follow up", "circle back"     | 0.58            |

Owner and due-date are inferred by separate patterns and, when found, add
bounded confidence bonuses (`+0.12` owner, `+0.10` due). "I'll take that"
attributes the owner to the current speaker. Due hints cover `by <weekday>`,
`by next week`, `by end of day/week/month`, `by eod` / `by eow`, `by tomorrow`
and `by <Month day>`.

## Provenance

Every decision and action carries a `Provenance` record:

- `rule_id` — which rule fired
- `trigger` — the exact matched phrase
- `utterance_indices` — the source spans (file-order indices)
- `note` — a human sentence explaining any inference

Confidence is always clipped to `[0.05, 0.99]` — the tool never claims
certainty it cannot justify.
