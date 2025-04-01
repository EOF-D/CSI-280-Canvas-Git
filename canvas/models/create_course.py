from __future__ import annotations

import asyncio
from attrs import define, field
from canvas import CanvasAuth, CanvasAPIClient, CanvasScope, Model
from typing import Dict, Any, Optional

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


      
