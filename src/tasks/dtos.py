from pydantic import BaseModel

class Task_schema(BaseModel):
    title: str
    description: str
    is_completed: bool = False


class Task_response_schema(BaseModel):
    id:int
    title: str
    description: str
    is_completed: bool
    user_id:int | None