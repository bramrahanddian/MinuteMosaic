"""Assemble a full MeetingReport from a transcript."""

from __future__ import annotations

import datetime as _dt
from typing import List

from .extract import extract_actions, extract_decisions
from .model import MeetingReport, Utterance
from .segment import segment_for_index, segment_topics


def build_report(
    utterances: List[Utterance],
