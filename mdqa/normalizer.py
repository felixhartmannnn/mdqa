from __future__ import annotations

import re
from typing import List


_HEADING_RE = re.compile(r"^(#{1,6})(\s+)(.+)$")


def normalize_headings(text: str) -> str:
    lines = text.splitlines()
    previous_level = 0
    out: List[str] = []
    for line in lines:
        match = _HEADING_RE.match(line)
        if match:
            level = len(match.group(1))
            title = match.group(3)
            if level <= previous_level:
                normalized = f"{'#' * level} {title}"
                out.append(normalized)
            else:
                out.append(line)
            previous_level = level
        else:
            out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")
