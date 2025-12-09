# Transcript format

minutemosaic consumes **JSON Lines** (`.jsonl`): one JSON object per line. It
does not produce transcripts and performs no audio processing — you bring a
transcript from whatever tool you already trust.

## Required fields

Each line is an object with timing, a speaker, and text. The loader is forgiving
about key spelling:

| Concept | Accepted keys                                   |
|---------|-------------------------------------------------|
| start   | `start`, `start_time`, `ts`, `t0`, `begin`      |
| end     | `end`, `end_time`, `t1`, `stop` (defaults to start) |
| speaker | `speaker`, `spk`, `who`, `name` (defaults `UNKNOWN`) |
| text    | `text`, `content`, `utterance`, `words` (list joined) |

Times are seconds from meeting start, as numbers.

## Rules

- Blank lines and lines starting with `#` are ignored (handy for fixtures).
- A line missing a start time or text is a hard error, reported with its line
  number. We never invent timing.
- Utterance `index` is assigned in file order and is the anchor for provenance.

## Example

```json
{"start": 0.0, "end": 4.2, "speaker": "Ada", "text": "Let's start."}
{"start": 4.5, "end": 9.1, "speaker": "Ravi", "text": "Build is green."}
```

See [`examples/product-sync.jsonl`](../examples/product-sync.jsonl).
