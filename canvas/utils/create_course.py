from __future__ import annotations

import asyncio
from attrs import define, field
from canvas import CanvasAuth, CanvasAPIClient, CanvasScope, Model
from typing import Dict, Any, Optional

@define
class User(Model):
    client: CanvasAPIClient = field()

    id: int
    name: str
    email: str

@define
class Course(Model):
    client: CanvasAPIClient = field()

    id: int
    name: str
    course_code: str
    account_id: int
    start_at: Optional[str] = None
    end_at: Optional[str] = None
    # Add other course attributes as needed

    @classmethod
    async def create(
        cls,
        client: CanvasAPIClient,
        account_id: int,
        course_data: Dict[str, Any],
        **kwargs
    ) -> Course:
        """
        Create a new course in the specified account.
        :param client: The Canvas API client
        :param account_id: The ID of the account where the course will be created
        :param course_data: A dictionary containing the course parameters
        :return: The created Course object
        """
        endpoint = f"accounts/{account_id}/courses"
        
        request_data = {
            "course": {
                "name": course_data["name"],  # Required field, no default
                "course_code": course_data["course_code"],  # Required field
                "start_at": course_data.get("start_at"),
                "end_at": course_data.get("end_at"),
                "license": course_data.get("license"),
                "is_public": course_data.get("is_public", False),
                "is_public_to_auth_users": course_data.get("is_public_to_auth_users", False),
                "public_syllabus": course_data.get("public_syllabus", False),
                "public_syllabus_to_auth": course_data.get("public_syllabus_to_auth", False),
                "public_description": course_data.get("public_description"),
            },
            "offer": course_data.get("offer", False),
            "enroll_me": course_data.get("enroll_me", False),
            "enable_sis_reactivation": course_data.get("enable_sis_reactivation", False),
        }
        
        response = await client.post(endpoint, json=request_data)
        course_json = response.json()  # Get JSON data from response
        return cls.from_json(course_json, client=client)
