from fastapi import FastAPI
from database import engine
import models
from routers.todos import todos
from routers.users import users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(todos.router)
app.include_router(users.router)
