# from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
import models
from routers.todos.schemas import BasicTodo, ShowTodo, Todo
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)

router.next_id = 1


# Get all todos
@router.get("/", response_model=list[ShowTodo])
async def get_all_todos(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(models.Todo).offset(skip).limit(limit).all()


# Get single to do
@router.get("/{todo_id}", response_model=ShowTodo)
async def get_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todo).filter(models.Todo.todo_id == todo_id).first()
    if db_todo is None:
        raise HTTPException(
            status_code=404,
            detail=f"Item number {todo_id} was not found"
        )
    return db_todo


# Create new to do
# todo: user_id should be provided automatically
@router.post("/", response_model=ShowTodo)
async def create_todo(user_todo: BasicTodo, user_id: int, db: Session = Depends(get_db)):
    db_todo = models.Todo(todo_id=router.next_id, user_id=user_id, completion=False, **user_todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    router.next_id += 1
    return db_todo


# Delete to do
@router.delete("/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todo).filter(models.Todo.todo_id == todo_id).first()
    if db_todo is None:
        raise HTTPException(
            status_code=404,
            detail=f"Item number {todo_id} was not found"
        )
    db.delete(db_todo)
    db.commit()
    router.next_id -= 1
    return


# Update completion of existing to do
@router.patch("/{todo_id}", response_model=ShowTodo)
async def update_todo_completion(todo_id: int, completed: bool = True, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todo).filter(models.Todo.todo_id == todo_id)
    if db_todo is None:
        raise HTTPException(
            status_code=404,
            detail=f"Item number {todo_id} was not found"
        )
    db_todo.update({'completion': completed})
    db.commit()
    return db_todo.first()

