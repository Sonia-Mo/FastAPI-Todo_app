from pydantic import BaseModel


class BasicTodo(BaseModel):
    todo: str
    description: str | None = None

    class Config:
        orm_mode = True


class ShowTodo(BasicTodo):
    todo_id: int
    completion: bool = False


class Todo(ShowTodo):
    username: str

