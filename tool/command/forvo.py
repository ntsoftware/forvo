import logging
import sys
from argparse import Namespace

from tool import Config


def clear_cache(args: Namespace, cfg: Config) -> None:
    logging.info("clear forvo cache")
    logging.info(f"sounds: {cfg.sounds_path}")
    sys.exit(0)


def update_cache(args: Namespace, cfg: Config) -> None:
    logging.info("update forvo cache")
    sys.exit(0)
