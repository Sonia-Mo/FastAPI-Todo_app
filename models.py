from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    todo_count = Column(Integer)

    todos = relationship("Todo", back_populates="user")


class Todo(Base):
    __tablename__ = "todos"

    todo_id = Column(Integer, primary_key=True, index=True)
    todo = Column(String, index=True)
    description = Column(String, index=True)
    completion = Column(Boolean)
    username = Column(String, ForeignKey("users.username"), primary_key=True)

    user = relationship("User", back_populates="todos")

