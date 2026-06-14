import csv
import logging
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


class Row:
    def __init__(self, index: int, row: list[str]) -> None:
        self._index = index
        self._row = row

    def __str__(self) -> str:
        return f"{self._index}: {self._row}"


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
        self._columns = []
        self._headers = []

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
                    self._columns = [
                        col.strip() for col in value.split(self._separator)
                    ]
                else:
                    logger.warning(
                        "%s:%d: ignore header line '{line.strip()}'",
                        path,
                        lineno,
                    )
            except ValueError:
                logger.exception(
                    "%s:%d: cannot parse line '%s'",
                    path,
                    lineno,
                    line.strip(),
                )

        logger.debug("separator: '%s'", _escape_str(self._separator))
        logger.debug("newline: '%s'", _escape_str(self._newline))
        logger.debug("columns: %s", self._columns)

        reader = csv.reader(lines, delimiter=self._separator)
        self._rows = list(reader)
        logger.debug("read %d rows", len(self._rows))

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
            yield Row(i, row)
