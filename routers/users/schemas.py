# from typing import Optional
# from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr


class UserIn(BaseModel):
    # id: Optional[UUID] = uuid4()
    id: int  # TODO: change back to UUID
    username: str
    password: str
    email: EmailStr


class UserOut(BaseModel):
    username: str
    email: EmailStr


class User(BaseModel):
    # id: Optional[UUID] = uuid4()
    id: int  # TODO: change back to UUID
    username: str
    hashed_password: str
    email: EmailStr

    class Config:
        orm_mode = True

