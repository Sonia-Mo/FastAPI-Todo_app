from fastapi import APIRouter, HTTPException
from models import BasicTodo, ShowTodo

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)

memory: list[ShowTodo] = []


# Get all todos
@router.get("/", response_model=list[ShowTodo])
async def get_all_todos():
    return memory


# Get single to do
@router.get("/{todo_id}", response_model=ShowTodo)
async def get_todo(todo_id: int):
    for elem in memory:
        if elem.todo_id == todo_id:
            return elem
    raise HTTPException(
        status_code=404,
        detail=f"Item number {todo_id} was not found"
    )


# Create new to do
@router.post("/{todo_id}", response_model=ShowTodo)
async def create_todo(user_todo: BasicTodo):
    next_id = len(memory) + 1
    todo = ShowTodo(todo_id=next_id, **user_todo.dict())
    memory.append(todo)
    return todo


# Delete to do
@router.delete("/{todo_id}")
async def delete_todo(todo_id: int):
    for elem in memory:
        if elem.todo_id == todo_id:
            memory.remove(elem)
            return
    raise HTTPException(
        status_code=404,
        detail=f"Item number {todo_id} was not found"
    )


# Update completion of existing to do
@router.patch("/{todo_id}", response_model=ShowTodo)
async def update_todo_completion(todo_id: int, completed: bool = True):
    for elem in memory:
        if elem.todo_id == todo_id:
            elem.completion = completed
            return elem
    raise HTTPException(
        status_code=404,
        detail=f"Item number {todo_id} was not found"
    )
