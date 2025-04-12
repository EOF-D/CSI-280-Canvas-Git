"""Canvas LMS Init Command.
============================

Implements init command for the CLI.
"""

from __future__ import annotations

from argparse import Namespace
from pathlib import Path
from canvasapi import Canvas
from canvasapi.user import User

from .base import CanvasCommand

__all__ = ("InitCommand",)


class InitCommand(CanvasCommand):
    """Command to initialize a canvas course."""

    def __init__(self, args: Namespace, client: Canvas, user: User) -> None:
        """Create init command instance from args.

        :param args: Command args.
        :type args: Namespace

        :param client: API client for when API calls are needed.
        :type client: Canvas

        :param client: User for API calls.
        :type client: User
        """
        self.client = client
        self.user = user
        self.course_id = args.course_id

    def _clone_course(self) -> None:
        """Get the course data from the API."""
        self.course = self.client.get_course(self.course_id)
        # if course_id not supplied, show them list and ask them to choose

    def _format_name(self, name):
        return "".join(x for x in name if x.isalnum())

    def execute(self) -> None:
        """Execute the command."""
        if self.course_id is None:
            print("--course_id flag is required")
            exit()

        print("Initializing course...")

        # Get course info from client
        self._clone_course()

        curr_dir = Path.cwd().absolute()
        course_dir = curr_dir / self._format_name(self.course.name)
        canvas_dir = course_dir / ".canvas"

        # Create .canvas folder
        canvas_dir.mkdir(parents=True, exist_ok=True)

        # Create files in .canvas folder
        (canvas_dir / "config.json").touch(exist_ok=True)
        (canvas_dir / "token.json").touch(exist_ok=True)
        (canvas_dir / "staged.json").touch(exist_ok=True)
        (canvas_dir / "metadata.json").touch(exist_ok=True)

        # Create modules folder
        print("Downloading modules...")
        modules_dir = course_dir / "modules"
        modules_dir.mkdir(parents=True, exist_ok=True)
        for module in self.course.get_modules():
            # Create module folder
            module_dir = modules_dir / self._format_name(module.name)
            module_dir.mkdir(parents=True, exist_ok=True)
            # Download assignments & files
            for item in module.get_module_items():
                if item.type == "Assignment":
                    # Create assignment and .info folder
                    assignment_dir = module_dir / self._format_name(item.title)
                    info_dir = assignment_dir / ".info"
                    assignment_dir.mkdir(parents=True, exist_ok=True)
                    info_dir.mkdir(parents=True, exist_ok=True)

                    # Download description
                    assignment = self.course.get_assignment(item.content_id)
                    (info_dir / "description.md").write_text(
                        assignment.description
                    )
                if item.type == "File":
                    # Download file
                    file = self.course.get_file(item.content_id)
                    file.download(str(module_dir / file.display_name))

        print(f"Course initialized at {course_dir}\n")
