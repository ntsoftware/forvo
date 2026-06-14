#!/usr/bin/env python3

import logging
from argparse import ArgumentParser

from tool import Config
from tool.command import clear_cache, update_cache
from tool.ui import run


def build_parser() -> ArgumentParser:
    common = ArgumentParser(add_help=False)
    common.add_argument(
        "-v", "--verbose", action="count", default=0, help="increase verbosity"
    )

    parser = ArgumentParser(description="TODO", parents=[common])
    parser.set_defaults(func=None)
    subparsers = parser.add_subparsers()

    clear_cache_parser = subparsers.add_parser(
        "clear-cache", help="clear forvo cache", parents=[common]
    )
    clear_cache_parser.set_defaults(func=clear_cache)

    update_cache_parser = subparsers.add_parser(
        "update-cache", help="update forvo cache", parents=[common]
    )
    update_cache_parser.set_defaults(func=update_cache)

    return parser


def configure_logging(verbose: int) -> None:
    if verbose == 0:
        level = logging.WARNING
    elif verbose == 1:
        level = logging.INFO
    else:
        level = logging.DEBUG

    logging.basicConfig(level=level, format="%(levelname)s  %(message)s")


args = build_parser().parse_args()

configure_logging(args.verbose)

cfg = Config()

if args.func:
    args.func(args, cfg)
else:
    run()
