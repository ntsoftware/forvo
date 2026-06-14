import csv
import logging
from pathlib import Path

from tool import Config


def _parse_separator(value: str) -> str:
    if value == "comma":
        return ","
    elif value == "semicolon":
        return ";"
    elif value == "tab":
        return "\t"
    elif value == "space":
        return " "
    elif value == "pipe":
        return "|"
    elif value == "colon":
        return ":"
    else:
        return value


def _escape_str(value: str) -> str:
    value = value.replace("\t", r"\t")
    value = value.replace("\r", r"\r")
    value = value.replace("\n", r"\n")
    return value


def _unescape_str(value: str) -> str:
    value = value.replace(r"\t", "\t")
    value = value.replace(r"\r", "\r")
    value = value.replace(r"\n", "\n")
    return value


class WordList:
    def __init__(self, path: Path, cfg: Config) -> None:
        logging.debug(f"read word list {path}")
        with open(path, newline="", encoding="utf-8") as fp:
            lines = [line for line in fp]

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
                    logging.warning(
                        f"{path}:{lineno}: ignore header line '{line.strip()}'"
                    )
            except ValueError:
                logging.error(f"{path}:{lineno}: cannot parse line '{line.strip()}'")

        logging.debug(f"separator: '{_escape_str(self._separator)}'")
        logging.debug(f"newline: '{_escape_str(self._newline)}'")
        logging.debug(f"columns: {self._columns}")

        reader = csv.reader(lines, delimiter=self._separator)
        self._rows = [row for row in reader]
        logging.debug(f"read {len(self._rows)} rows")

    def save(self, path: Path) -> None:
        logging.debug(f"write word list {path}")
        with open(path, mode="w", newline="", encoding="utf-8") as fp:
            for line in self._headers:
                fp.write(line)

            writer = csv.writer(
                fp, delimiter=self._separator, lineterminator=self._newline
            )
            writer.writerows(self._rows)
            logging.debug(f"wrote {len(self._rows)} rows")

    def __iter__(self):
        return iter(self._rows)
