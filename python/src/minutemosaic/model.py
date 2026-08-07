"""Core data model for minutemosaic.

All structures are plain dataclasses so they serialize cleanly to JSON and stay
inspectable. Time is stored as float seconds from meeting start; we never invent
timestamps that were not present in the input.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class Utterance:
    """A single timestamped, attributed line of transcript.

    ``index`` is the stable 0-based position within the loaded transcript and is
    the atomic unit of provenance: every derived claim references one or more
    utterance indices (its *source spans*).
    """

    index: int
    start: float
    end: float
    speaker: str
    text: str

    @property
    def duration(self) -> float:
        return max(0.0, self.end - self.start)

    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)


@dataclass(frozen=True)
class Provenance:
    """Evidence attached to a derived claim.

    A claim is only as trustworthy as the spans it points at, so we keep the
    exact utterance indices, the matched trigger phrase and the heuristic rule id
    that fired. This is what makes the output auditable rather than magical.
    """

    rule_id: str
    trigger: str
    utterance_indices: List[int]
    note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)


@dataclass
class TopicSegment:
    """A contiguous run of utterances judged to share a topic."""

    segment_id: int
    start_index: int
    end_index: int  # inclusive
    start_time: float
    end_time: float
    label: str
    keywords: List[str] = field(default_factory=list)
    speakers: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "segment_id": self.segment_id,
            "start_index": self.start_index,
            "end_index": self.end_index,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "label": self.label,
            "keywords": self.keywords,
            "speakers": self.speakers,
        }


@dataclass
class Decision:
    decision_id: int
    text: str
    speaker: str
    time: float
    segment_id: Optional[int]
    confidence: float
    provenance: Provenance

    def to_dict(self) -> Dict[str, Any]:
        d = dataclasses.asdict(self)
        d["provenance"] = self.provenance.to_dict()
        return d


@dataclass
class ActionItem:
    action_id: int
    text: str
    owner: Optional[str]
    due_hint: Optional[str]
    speaker: str
    time: float
    segment_id: Optional[int]
    confidence: float
    provenance: Provenance

    def to_dict(self) -> Dict[str, Any]:
        d = dataclasses.asdict(self)
        d["provenance"] = self.provenance.to_dict()
        return d


@dataclass
class MeetingReport:
    title: str
    generated_at: str
    source: str
    utterances: List[Utterance]
    segments: List[TopicSegment]
    decisions: List[Decision]
    actions: List[ActionItem]
    stats: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema": "minutemosaic/report/v1",
            "title": self.title,
            "generated_at": self.generated_at,
            "source": self.source,
            "stats": self.stats,
            "utterances": [u.to_dict() for u in self.utterances],
            "segments": [s.to_dict() for s in self.segments],
            "decisions": [d.to_dict() for d in self.decisions],
            "actions": [a.to_dict() for a in self.actions],
        }
