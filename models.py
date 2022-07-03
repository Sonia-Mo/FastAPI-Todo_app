from pydantic import BaseModel, EmailStr


class BasicTodo(BaseModel):
    todo: str
    description: str | None = None


class ShowTodo(BasicTodo):
    todo_id: int
    completion: bool = False


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserOut(BaseModel):
    username: str
    email: EmailStr


# class UserInDB(BaseModel):
#     username: str
#     hashed_password: str
#     email: EmailStr
