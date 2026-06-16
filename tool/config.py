import logging
import sys
from configparser import ConfigParser
from pathlib import Path

logger = logging.getLogger()


def get_default_config_path() -> Path:
    assets = getattr(sys, "_MEIPASS", "assets")
    return Path(assets).joinpath("defaults.ini").resolve()


def get_user_config_path() -> Path:
    return Path("~/.jptool/config.ini").expanduser()


class Config:
    def __init__(self) -> None:
        default_path = get_default_config_path()
        user_path = get_user_config_path()
        logger.debug("default config path: %s", default_path)
        logger.debug("user config path: %s", user_path)

        self._cfg = ConfigParser()
        if default_path.exists():
            logger.debug("read default config file %s", default_path)
            self._cfg.read(default_path)
        if user_path.exists():
            logger.debug("read user config file %s", user_path)
            self._cfg.read(user_path)

    @property
    def wordlist_separator(self) -> str:
        return self._cfg.get("wordlist", "separator")

    @property
    def wordlist_newline(self) -> str:
        return self._cfg.get("wordlist", "newline")

    @property
    def wordlist_ja_columns(self) -> list[str]:
        return self._cfg.get("wordlist", "ja_columns").split()

    @property
    def wordlist_sound_columns(self) -> list[str]:
        return self._cfg.get("wordlist", "sound_columns").split()

    @property
    def forvo_cache(self) -> Path:
        return Path(self._cfg.get("forvo", "cache")).expanduser().resolve()

    @property
    def forvo_preferred_users(self) -> list[str]:
        return self._cfg.get("forvo", "preferred_users").split()

    @property
    def forvo_preferred_countries(self) -> list[str]:
        return self._cfg.get("forvo", "preferred_countries").split()

    @property
    def sounds_path(self) -> Path:
        return Path(self._cfg.get("sounds", "path")).expanduser().resolve()
