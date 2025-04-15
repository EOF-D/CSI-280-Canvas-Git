"""Canvas LMS Argument Parser.
============================

Implements an argument parser for the CLI.
"""

from __future__ import annotations

from argparse import ArgumentParser

from .. import __version__

__all__ = ("get_parser",)


def get_parser() -> ArgumentParser:
    """Creates the argument parser for the CLI.
    This is how we'll interact with the Canvas LMS API.

    :return: The `ArgumentParser` with the necessary arguments.
    :rtype: ArgumentParser
    """

    parser = ArgumentParser(prog="canvas")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"Canvas Git: {__version__}",
    )

    subparser = parser.add_subparsers(dest="command", help="Commands")

    # Subparser for each command
    init_parser = subparser.add_parser("init", help="Initialize the course")
    init_parser.add_argument(
        "-c", "--course_id", help="ID of the canvas course to download"
    )

    add_cmd_parser = subparser.add_parser(
        "add", help="Add a file to be tracked"
    )
    add_cmd_parser.add_argument(
        "-f", "--file_path", help="Path of the file to be tracked"
    )

    return parser
