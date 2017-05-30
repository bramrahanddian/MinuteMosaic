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

