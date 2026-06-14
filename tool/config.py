import logging
import sys
from configparser import ConfigParser
from pathlib import Path
from typing import List


def get_default_config_path() -> Path:
    assets = getattr(sys, "_MEIPASS", "assets")
    return Path(assets).joinpath("defaults.ini").resolve()


def get_user_config_path() -> Path:
    return Path("~/.jptool/config.ini").expanduser()


class Config:
    def __init__(self) -> None:
        default_path = get_default_config_path()
        user_path = get_user_config_path()
        logging.debug(f"default config path: {default_path}")
        logging.debug(f"user config path: {user_path}")

        self._cfg = ConfigParser()
        if default_path.exists():
            logging.debug(f"read default config file {default_path}")
            self._cfg.read(default_path)
        if user_path.exists():
            logging.debug(f"read user config file {user_path}")
            self._cfg.read(user_path)

    @property
    def wordlist_separator(self) -> str:
        return self._cfg.get("wordlist", "separator")

    @property
    def wordlist_newline(self) -> str:
        return self._cfg.get("wordlist", "newline")

    @property
    def forvo_cache(self) -> Path:
        return Path(self._cfg.get("forvo", "cache")).expanduser().resolve()

    @property
    def forvo_preferred_users(self) -> List[str]:
        return self._cfg.get("forvo", "preferred_users").split()

    @property
    def forvo_preferred_countries(self) -> List[str]:
        return self._cfg.get("forvo", "preferred_countries").split()

    @property
    def sounds_path(self) -> Path:
        return Path(self._cfg.get("sounds", "path")).expanduser().resolve()
