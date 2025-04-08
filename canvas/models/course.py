from __future__ import annotations

from attrs import define, field
from ..rest import CanvasAPIClient
from .base import Model

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

 def update_course(self, course_id, course_params):
        """
        Update a single course using the Canvas API.
        :param course_id: ID of the course to update
        :param course_params: Dictionary of course parameters to update
        :return: JSON response from the API
        """
        url = f"{self.base_url}/api/v1/courses/{course_id}"
        response = requests.put(url, headers=self.headers, json={"course": course_params})
        return response.json()

    def batch_update_courses(self, account_id, course_ids, event):
        """
        Batch update multiple courses using the Canvas API.
        :param account_id: ID of the account containing the courses
        :param course_ids: List of course IDs to update
        :param event: Action to take on each course ('offer', 'conclude', 'delete', 'undelete')
        :return: JSON response from the API (Progress object)
        """
        url = f"{self.base_url}/api/v1/accounts/{account_id}/courses"
        data = {
            "course_ids[]": course_ids,
            "event": event
        }
        response = requests.put(url, headers=self.headers, data=data)
        return response.json()
