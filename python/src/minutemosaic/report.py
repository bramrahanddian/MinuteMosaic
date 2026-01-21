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
    for u in utterances:
        talk_time[u.speaker] = round(talk_time.get(u.speaker, 0.0) + u.duration, 2)

    stats = {
        "utterance_count": len(utterances),
        "segment_count": len(segments),
        "decision_count": len(decisions),
        "action_count": len(actions),
        "speakers": speakers,
        "meeting_span_seconds": round(total_time, 2),
        "talk_time_seconds": talk_time,
    }

    return MeetingReport(
        title=title,
        generated_at=_dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        source=source,
        utterances=utterances,
        segments=segments,
        decisions=decisions,
        actions=actions,
        stats=stats,
    )

# draft note 1394
