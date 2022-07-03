from fastapi import FastAPI, HTTPException
from models import BasicTodo, ShowTodo

app = FastAPI()

memory: list[ShowTodo] = []


# =========================== CRUD Methods on todos ===========================

# Get all todos
@app.get("/", response_model=list[ShowTodo])
async def get_all_todos():
    return memory


# Get single to do
@app.get("/{todo_id}", response_model=ShowTodo)
async def get_todo(todo_id: int):
    for elem in memory:
        if elem.todo_id == todo_id:
            return elem
    raise HTTPException(
        status_code=404,
        detail=f"item number {todo_id} was not found"
    )


# Create new to do
@app.post("/{todo_id}", response_model=ShowTodo)
async def create_todo(user_todo: BasicTodo):
    next_id = len(memory) + 1
    todo = ShowTodo(todo_id=next_id, **user_todo.dict())
    memory.append(todo)
    return todo


# Delete to do
@app.delete("/{todo_id}")
async def delete_todo(todo_id: int):
    for elem in memory:
        if elem.todo_id == todo_id:
            memory.remove(elem)
            return
    raise HTTPException(
        status_code=404,
        detail=f"item number {todo_id} was not found"
    )


# Update completion of existing to do
@app.patch("/{todo_id}", response_model=ShowTodo)
async def update_todo_completion(todo_id: int, completed: bool = True):
    for elem in memory:
        if elem.todo_id == todo_id:
            elem.completion = completed
            return elem
    raise HTTPException(
        status_code=404,
        detail=f"item number {todo_id} was not found"
    )
