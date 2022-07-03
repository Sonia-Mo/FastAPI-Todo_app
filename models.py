from pydantic import BaseModel


class BasicTodo(BaseModel):
    todo: str
    description: str | None = None


class ShowTodo(BasicTodo):
    todo_id: int
    completion: bool = False

