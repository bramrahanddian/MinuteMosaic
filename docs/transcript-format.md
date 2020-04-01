# Transcript format

minutemosaic consumes **JSON Lines** (`.jsonl`): one JSON object per line. It
does not produce transcripts and performs no audio processing — you bring a
transcript from whatever tool you already trust.

## Required fields

Each line is an object with timing, a speaker, and text. The loader is forgiving
about key spelling:

