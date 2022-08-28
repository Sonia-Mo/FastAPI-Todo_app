from pydantic import BaseModel
from typing import Optional


class BasicTodo(BaseModel):
    todo: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


class ShowTodo(BasicTodo):
    todo_id: int
    completion: bool = False


class Todo(ShowTodo):
    username: str

