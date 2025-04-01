from __future__ import annotations

from attrs import define, field
from canvas import CanvasAuth, CanvasAPIClient, CanvasScope, Model

__all__ = ("Course",)


@define
class Course(Model):
    client: CanvasAPIClient = field()

    id: int
    name: str
    course_code: str
    account_id: int
    start_at: str | None
    end_at: str | None
    # Add other course attributes as needed


      
