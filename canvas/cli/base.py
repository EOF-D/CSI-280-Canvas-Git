"""Canvas LMS Base Command.
============================

Implements the base command for the CLI.
"""

from __future__ import annotations

import json
import pickle
from typing import Any
from abc import ABC, abstractmethod
from pathlib import Path

from cryptography.fernet import Fernet

from .. import OAuthToken
from ..errors import CLIError

__all__ = (
    "CanvasCommand",
    "NotCanvasCourseException",
)


class NotCanvasCourseException(CLIError):
    """Raised when a command is run outside a canvas course.

    Note that not all commands need to be run from inside a canvas course.
    """


class TokenCacheException(CLIError):
    """Raised when a token isn't cached."""


class CanvasCommand(ABC):
    """Canvas git command which can be executed."""

    @classmethod
    def get_current_dir(cls) -> Path:
        return Path.cwd().resolve()

    @classmethod
    def get_rel_path(cls, path: Path) -> Path:
        return path.relative_to(cls.get_current_dir(), walk_up=True)

    @classmethod
    def get_course_root(cls) -> Path:
        """Find the root directory of the course.

        :raises NotCanvasCourseException: Not inside a canvas course.

        :return: Path to the course's root directory (contains .canvas).
        :rtype: Path
        """
        curr_dir = cls.get_current_dir()

        # Search through parent directories for .canvas folder
        while not (curr_dir / ".canvas").exists():
            curr_dir = curr_dir.parent

            # If root reached, command wasn't run from within course
            if curr_dir == curr_dir.parent:
                raise NotCanvasCourseException

        return curr_dir.resolve()

    @classmethod
    def get_course_canvas_dir(cls) -> Path:
        """Find the .canvas directory of the course.

        :raises NotCanvasCourseException: Not inside a canvas course.

        :return: Path to the course's .canvas directory.
        :rtype: Path
        """
        return cls.get_course_root() / ".canvas"

    @classmethod
    def get_metadata(cls, key: str) -> Any:
        """Get course metadata given a key.

        :raises NotCanvasCourseException: Not inside a canvas course.
        :raises KeyError: Key not found in metadata.

        :return: The metadata value.
        :rtype: Any
        """
        canvas_folder = cls.get_course_canvas_dir()

        metadata_file = canvas_folder / "metadata.json"

        with open(metadata_file, "r") as f:
            metadata = json.load(f)

        if key in metadata:
            return metadata[key]
        else:
            raise KeyError

    @classmethod
    def find_first_tracked_parent(cls, path: Path) -> tuple[Path, Any]:
        tracked = None
        while tracked is None:
            path = path.parent
            tracked = cls.get_metadata(str(path.absolute()))

        return path, tracked

    @classmethod
    def load_fernet_key(cls) -> bytes:
        canvas_folder = cls.get_course_canvas_dir()
        with open(canvas_folder / "key.key", "rb") as key_file:
            key = key_file.read()
        return key

    @classmethod
    def load_token(cls) -> OAuthToken:
        canvas_folder = cls.get_course_canvas_dir()

        token_file = canvas_folder / "token.pickle"

        key = cls.load_fernet_key()
        fernet = Fernet(key)

        with open(token_file, "rb") as f:
            encrypted_token = f.read()

        if not encrypted_token:
            raise TokenCacheException

        pickled_token = fernet.decrypt(encrypted_token)
        token = pickle.loads(pickled_token)

        return token

    @classmethod
    def save_token(cls, token: OAuthToken) -> None:
        canvas_folder = cls.get_course_canvas_dir()

        token_file = canvas_folder / "token.pickle"

        pickled_token = pickle.dumps(token)

        key = cls.load_fernet_key()
        fernet = Fernet(key)

        encrypted_token = fernet.encrypt(pickled_token)

        with open(token_file, "wb") as f:
            f.write(encrypted_token)

    @abstractmethod
    def execute(self) -> None:
        """Execute the command."""
        pass
