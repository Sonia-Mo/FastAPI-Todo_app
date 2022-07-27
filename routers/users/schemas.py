from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserIn(BaseUser):
    password: str


class UserOut(BaseUser):
    pass


class User(BaseUser):
    hashed_password: str
    todo_count: int = 0

