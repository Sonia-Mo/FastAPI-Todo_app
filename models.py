from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # TODO: change back to UUID
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    todos = relationship("Todo", back_populates="user")


class Todo(Base):
    __tablename__ = "todos"

    todo_id = Column(Integer, primary_key=True, index=True)
    todo = Column(String, index=True)
    description = Column(String, index=True)
    completion = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id"))  # TODO: change back to UUID

    user = relationship("User", back_populates="todos")

