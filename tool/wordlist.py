import csv
import logging
import re
from collections.abc import Iterator
from pathlib import Path

from tool import Config

logger = logging.getLogger()


def _parse_separator(value: str) -> str:
    delimiters = {
        "comma": ",",
        "semicolon": ";",
        "tab": "\t",
        "space": " ",
        "pipe": "|",
        "colon": ":",
    }
    return delimiters.get(value, value)


def _escape_str(value: str) -> str:
    return value.replace("\t", r"\t").replace("\r", r"\r").replace("\n", r"\n")


def _unescape_str(value: str) -> str:
    return value.replace(r"\t", "\t").replace(r"\r", "\r").replace(r"\n", "\n")


def _is_japanese_text(value: str) -> bool:
    n = sum([_is_japanese_char(char) for char in value])
    return n > len(value) // 2


def _is_japanese_char(char: str) -> bool:
    return (
        _is_japanese_punctuation(char)
        or _is_hiragna(char)
        or _is_katakana(char)
        or _is_kanji(char)
    )


def _is_japanese_punctuation(char: str) -> bool:
    first = 0x3000
    last = 0x303F
    return first <= ord(char) <= last


def _is_hiragna(char: str) -> bool:
    first = 0x3040
    last = 0x309F
    return first <= ord(char) <= last


def _is_katakana(char: str) -> bool:
    first = 0x30A0
    last = 0x30FF
    return first <= ord(char) <= last


def _is_kanji(char: str) -> bool:
    first = 0x4E00
    last = 0x9FFF
    return first <= ord(char) <= last


def _guess_japanese_columns(rows: list[list[str]]) -> list[int]:
    column_indices: set[int] = set()
    for row in rows:
        for i, value in enumerate(row):
            if _is_japanese_text(value):
                column_indices.add(i)
    return sorted(column_indices)


def _get_sound_files(value: str) -> list[str]:
    return re.findall(r"\[sound:([^\]]+)\]", value)


def _guess_sound_columns(rows: list[list[str]]) -> list[int]:
    column_indices: set[int] = set()
    for row in rows:
        for i, value in enumerate(row):
            if _get_sound_files(value):
                column_indices.add(i)
    if column_indices:
        return sorted(column_indices)
    return [max([len(row) for row in rows])]


def _get_column_indices(columns: list[str], selected: list[str]) -> list[int]:
    column_indices: list[int] = []
    for value in selected:
        if value in columns:
            column_indices.append(columns.index(value))
        else:
            logger.warning("column '%s' not found", value)
    return column_indices


class Row:
    def __init__(
        self,
        index: int,
        values: list[str],
        ja_columns: list[int],
        sound_columns: list[int],
    ) -> None:
        self._index = index
        self._values = values
        self._ja_columns = ja_columns
        self._sound_columns = sound_columns

    def __str__(self) -> str:
        return f"{self._index}: {self._values}"

    def _get_values(self, column_indices: list[int]) -> list[str]:
        return [
            self._values[i]
            for i in column_indices
            if i < len(self._values) and self._values[i]
        ]

    @property
    def japanese_words(self) -> list[str]:
        return self._get_values(self._ja_columns)

    @property
    def sound_files(self) -> list[str]:
        return [
            sound_file
            for value in self._get_values(self._sound_columns)
            for sound_file in _get_sound_files(value)
        ]

    @property
    def index(self) -> int:
        return self._index


class WordList:
    def __init__(self, path: Path, cfg: Config) -> None:
        logger.debug("read word list %s", path)
        with path.open(newline="", encoding="utf-8") as fp:
            lines = list(fp)

            if fp.newlines is None:
                self._newline = _unescape_str(cfg.wordlist_newline)
            elif isinstance(fp.newlines, str):
                self._newline = fp.newlines
            else:
                self._newline = fp.newlines[0]

        self._separator = cfg.wordlist_separator
        self._columns: list[str] = []
        self._headers: list[str] = []

        lineno = 0
        while lines and lines[0].startswith("#"):
            line = lines.pop(0)
            lineno += 1
            self._headers.append(line)
            try:
                key, value = line.removeprefix("#").lower().split(":")
                if key == "separator":
                    self._separator = _parse_separator(value.strip())
                elif key == "columns":
                    self._columns = [s.strip() for s in value.split(self._separator)]
                else:
                    logger.warning(
                        "%s:%d: ignore header line '%s'",
                        path,
                        lineno,
                        line.strip(),
                    )
            except ValueError:
                logger.exception(
                    "%s:%d: cannot parse line '%s'",
                    path,
                    lineno,
                    line.strip(),
                )

        reader = csv.reader(lines, delimiter=self._separator)
        self._rows = list(reader)
        logger.debug("read %d rows", len(self._rows))

        if self._columns:
            self._ja_columns = _get_column_indices(
                self._columns,
                cfg.wordlist_ja_columns,
            )
            self._sound_columns = _get_column_indices(
                self._columns,
                cfg.wordlist_sound_columns,
            )
        else:
            self._ja_columns = _guess_japanese_columns(self._rows)
            self._sound_columns = _guess_sound_columns(self._rows)

        logger.debug("separator: '%s'", _escape_str(self._separator))
        logger.debug("newline: '%s'", _escape_str(self._newline))
        logger.debug("columns: %s", self._columns)
        logger.debug("ja_columns: %s", self._ja_columns)
        logger.debug("sound_columns: %s", self._sound_columns)

    def save(self, path: Path) -> None:
        logger.debug("write word list %s", path)
        with path.open(mode="w", newline="", encoding="utf-8") as fp:
            fp.writelines(self._headers)

            writer = csv.writer(
                fp,
                delimiter=self._separator,
                lineterminator=self._newline,
            )
            writer.writerows(self._rows)
            logger.debug("wrote %d rows", len(self._rows))

    def __iter__(self) -> Iterator[Row]:
        for i, row in enumerate(self._rows):
            yield Row(i, row, self._ja_columns, self._sound_columns)
