import sys
from pathlib import Path

def asset(path: str) -> Path:
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS).joinpath(path)
    else:
        return Path("assets").joinpath(path)
