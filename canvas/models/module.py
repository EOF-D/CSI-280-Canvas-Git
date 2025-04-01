from __future__ import annotations

from attrs import define, field
from canvas import CanvasAuth, CanvasAPIClient, CanvasScope, Model
from datetime import datetime

__all__ = ("Course",)


@define
class Module(Model):
    client: CanvasAPIClient = field()
    
    id: int
    name: str
    position: int
    unlock_at: str | None
    require_sequential_progress: bool
    prerequisite_module_ids: list[int]
    publish_final_grade: bool
