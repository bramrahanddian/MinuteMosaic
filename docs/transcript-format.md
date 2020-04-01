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
