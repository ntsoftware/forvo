import logging
import sys
from argparse import Namespace

from tool import Config, WordList, query

logger = logging.getLogger()


def clear_cache(_args: Namespace, _cfg: Config) -> None:
    logger.info("clear forvo cache")
    sys.exit(0)


def update_cache(_args: Namespace, _cfg: Config) -> None:
    logger.info("update forvo cache")
    sys.exit(0)


def get_queries(args: Namespace, cfg: Config) -> None:
    for row in WordList(args.file, cfg):
        for i, word in enumerate(row.japanese_words):
            queries = query.split(word)
            print(f"{row.index}:{i} {word} => [{','.join(queries)}]")  # noqa: T201
    sys.exit(0)
