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
