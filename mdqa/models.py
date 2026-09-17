from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Section:
    title: str
    lineno: int
    level: int
    content_lines: List[str] = field(default_factory=list)
    link_targets: List[str] = field(default_factory=list)
    end_lineno: Optional[int] = None


@dataclass
class Issue:
    code: str = ""
    message: str = ""
    lineno: int = 0
    context: str = ""
    skipped_level: int = 0
    previous_level: int = 0
    to_level: int = 0
    from_level: int = 0
    target: str = ""
    section_level: int = 0


@dataclass
class HeadingGapIssue(Issue):
    code: str = "MQ001"


@dataclass
class UnclosedHeadingGapIssue(Issue):
    code: str = "MQ002"


    section_level: int = 0


@dataclass
class EmptySectionIssue(Issue):
    code: str = "MQ003"


@dataclass
class LinkTargetIssue(Issue):
    code: str = "MQ004"
