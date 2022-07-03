from fastapi import FastAPI, HTTPException
from models import BasicTodo, ShowTodo
from routers import todos

app = FastAPI()

app.include_router(todos.router)
