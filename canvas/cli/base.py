"""Canvas LMS Base Command.
============================

Implements the base command for the CLI.
"""

from __future__ import annotations

import json
from typing import Any
from abc import ABC, abstractmethod
from pathlib import Path

from ..errors import CLIError

__all__ = (
    "CanvasCommand",
    "NotCanvasCourseException",
)


class NotCanvasCourseException(CLIError):
    """Raised when a command is run outside a canvas course.

    Note that not all commands need to be run from inside a canvas course.
    """


class CanvasCommand(ABC):
    """Canvas git command which can be executed."""

    @classmethod
    def find_course_root(cls) -> Path:
        """Find the root directory of the course.

        :return: Path to the course's root directory (contains .canvas).
        :rtype: Path
        """
        curr_dir = Path.cwd().absolute()

        # Search through parent directories for .canvas folder
        while not (curr_dir / ".canvas").exists():
            curr_dir = curr_dir.parent

            # If root reached, command wasn't run from within course
            if curr_dir == curr_dir.parent:
                raise NotCanvasCourseException

        return curr_dir

    @classmethod
    def get_metadata(cls, key: str) -> Any:
        root = cls.find_course_root()

        canvas_folder = root / ".canvas"
        metadata_file = canvas_folder / "metadata.json"

        with open(metadata_file, "r") as f:
            metadata = json.load(f)

        if key in metadata:
            return metadata[key]

        return None

    @classmethod
    def find_first_tracked_parent(cls, path: Path) -> tuple[Path, Any]:
        tracked = None
        while tracked is None:
            path = path.parent
            tracked = cls.get_metadata(str(path))

        return path, tracked

    @abstractmethod
    def execute(self) -> None:
        """Execute the command."""
        pass
