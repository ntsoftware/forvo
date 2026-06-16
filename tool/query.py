# ruff: noqa: RUF001

import re

_REPLACEMENTS: list[tuple[str, str]] = [
    (" ", ""),
    ("　", ""),
    ("。", ""),
    ("０", "0"),
    ("１", "1"),
    ("２", "2"),
    ("３", "3"),
    ("４", "4"),
    ("５", "5"),
    ("６", "6"),
    ("７", "7"),
    ("８", "8"),
    ("９", "9"),
]


def split(value: str) -> list[str]:
    s = value
    for x, y in _REPLACEMENTS:
        s = s.replace(x, y)

    parts = re.split(r"［(.*)］", s)

    if len(parts) == 1:
        s = s.removeprefix("～")
        return [s]
    if len(parts) == 3:
        a, b, c = parts
        if not a:
            s = b + c
            return [s]
        if not c and b.endswith("～"):
            s = b[:-1] + a
            return [s]
        if not c:
            s = a + b
            return [s]

    return [value]
