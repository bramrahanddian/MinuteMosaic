"""Transcript ingestion.

Input format: JSON Lines (JSONL), one utterance object per line. Each object
must carry a speaker, text and timing. We accept a couple of common key
spellings to be forgiving, but we never fabricate missing timing — a line
without usable timestamps is rejected with a clear, line-numbered error.

Example line::

    {"start": 12.4, "end": 15.9, "speaker": "Ada", "text": "Let's ship Friday."}
