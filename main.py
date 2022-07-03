from fastapi import FastAPI
from routers import todos, users


app = FastAPI()

app.include_router(todos.router)
app.include_router(users.router)
