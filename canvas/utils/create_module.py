from __future__ import annotations

import asyncio
from attrs import define, field
from canvas import CanvasAuth, CanvasAPIClient, CanvasScope, Model
from datetime import datetime
from typing import List, Optional

@define
class User(Model):
    client: CanvasAPIClient = field()
    id: int
    name: str
    email: str

@define
class Module(Model):
    client: CanvasAPIClient = field()
    
    id: int
    name: str
    position: int
    unlock_at: Optional[str] = None
    require_sequential_progress: bool = False
    prerequisite_module_ids: List[int] = field(factory=list)
    publish_final_grade: bool = False

    @classmethod
    async def create(
        cls,
        client: CanvasAPIClient,
        course_id: int,
        name: str,
        position: int,
        unlock_at: Optional[datetime] = None,
        require_sequential_progress: bool = False,
        prerequisite_module_ids: Optional[List[int]] = None,
        publish_final_grade: bool = False
    ) -> Module:
        url = f'courses/{course_id}/modules'
        
        data = {
            'module[name]': name,
            'module[position]': position,
            'module[require_sequential_progress]': require_sequential_progress,
            'module[publish_final_grade]': publish_final_grade
        }
        
        if unlock_at:
            data['module[unlock_at]'] = unlock_at.isoformat()
        
        if prerequisite_module_ids:
            for i, module_id in enumerate(prerequisite_module_ids):
                data[f'module[prerequisite_module_ids][{i}]'] = module_id
        
        response = await client.post(url, data=data)
        return cls.from_json(response, client=client)

async def main() -> None:
    scopes = (
        CanvasScope.GET_USER_PROFILE |
        CanvasScope.SHOW_ACCESS_TOKEN |
        CanvasScope.CREATE_ACCESS_TOKEN |
        CanvasScope.UPDATE_ACCESS_TOKEN |
        CanvasScope.DELETE_ACCESS_TOKEN |
        CanvasScope.MANAGE_COURSES
    )

    auth = CanvasAuth(
        client_id="",
        client_secret="",
        canvas_domain="eof-d.codes",
        scopes=scopes,
    )

    await auth.authenticate()
    async with CanvasAPIClient(auth) as client:
        # Get user example
        user = User.from_json(await client.get("users/1"), client=client)
        print("UserID: ", user.id)
        print(f"User: {user.name} ({user.email})")

        # Create module example
        new_module = await Module.create(
            client=client,
            course_id=123,  # Replace with actual course ID
            name="New Module Name",
            position=2,
            unlock_at=datetime.now(),
            require_sequential_progress=True,
            prerequisite_module_ids=[121, 122],
            publish_final_grade=False
        )
        print(f"Created module: {new_module.name} (ID: {new_module.id})")

if __name__ == "__main__":
    asyncio.run(main())
