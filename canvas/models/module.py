from __future__ import annotations

from attrs import define, field
from ..rest import CanvasAPIClient
from .base import Model

__all__ = ("Module",)


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
