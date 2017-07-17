"""Assemble a full MeetingReport from a transcript."""

from __future__ import annotations

import datetime as _dt
from typing import List

from .extract import extract_actions, extract_decisions
from .model import MeetingReport, Utterance
from .segment import segment_for_index, segment_topics


def build_report(
    utterances: List[Utterance],
    *,
    title: str,
    source: str,
    cohesion_threshold: float = 0.12,
    silence_gap: float = 8.0,
) -> MeetingReport:
    segments = segment_topics(
        utterances, cohesion_threshold=cohesion_threshold, silence_gap=silence_gap
    )

    def segment_of(index: int):
        return segment_for_index(segments, index)

    decisions = extract_decisions(utterances, segment_of)
    actions = extract_actions(utterances, segment_of)

    speakers = sorted({u.speaker for u in utterances})
    total_time = utterances[-1].end - utterances[0].start if utterances else 0.0
    talk_time = {}
