# Heuristics & provenance

The whole point of minutemosaic is that you can **read every rule** and predict
its output. There is no learned model and no hidden state.

## Topic segmentation

Boundaries between topics are opened when either:

1. **Cohesion drops.** We build a keyword bag (content words, stopwords removed)
   for a sliding window of recent utterances and compare it to the next
