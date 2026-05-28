from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str = None
    completed: bool = False

