import logging
import sys
from argparse import Namespace

from tool import Config

logger = logging.getLogger()


def clear_cache(_args: Namespace, _cfg: Config) -> None:
    logger.info("clear forvo cache")
    sys.exit(0)


def update_cache(_args: Namespace, _cfg: Config) -> None:
    logger.info("update forvo cache")
    sys.exit(0)
