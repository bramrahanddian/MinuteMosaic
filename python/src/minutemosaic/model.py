"""Core data model for minutemosaic.

All structures are plain dataclasses so they serialize cleanly to JSON and stay
inspectable. Time is stored as float seconds from meeting start; we never invent
timestamps that were not present in the input.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

