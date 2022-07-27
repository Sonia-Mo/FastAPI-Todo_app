from fastapi import APIRouter, HTTPException, Depends
import models
from authentication import get_current_user
from routers.todos.schemas import BasicTodo, ShowTodo
from sqlalchemy.orm import Session
from database import get_db
from routers.users.schemas import UserIn

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)


# Get all todos
@router.get("/", response_model=list[ShowTodo])
async def get_all_todos(db: Session = Depends(get_db),
                        user: UserIn = Depends(get_current_user),
                        skip: int = 0, limit: int = 100):

    return db.query(models.Todo).filter(models.Todo.username == user.username).offset(skip).limit(limit).all()


# Get single to do
@router.get("/{todo_id}", response_model=ShowTodo)
async def get_todo(todo_id: int,
                   user: UserIn = Depends(get_current_user),
                   db: Session = Depends(get_db)):

    db_todo = db.query(models.Todo).filter(models.Todo.username == user.username).\
        filter(models.Todo.todo_id == todo_id).first()
    if db_todo is None:
        raise HTTPException(
            status_code=404,
            detail=f"Item number {todo_id} was not found"
        )
    return db_todo


# Create new to do
@router.post("/", response_model=ShowTodo)
async def create_todo(user_todo: BasicTodo,
                      user: UserIn = Depends(get_current_user),
                      db: Session = Depends(get_db)):

    next_id = db.query(models.User.todo_count).filter(models.User.username == user.username).as_scalar()
    db_todo = models.Todo(todo_id=next_id + 1, username=user.username, completion=False, **user_todo.dict())
    db.add(db_todo)
    update_row = db.query(models.User).filter(models.User.username == user.username)
    update_row.update({'todo_count': (next_id + 1)})
    db.commit()
    return db_todo


# Delete to do
@router.delete("/{todo_id}")
async def delete_todo(todo_id: int,
                      user: UserIn = Depends(get_current_user),
                      db: Session = Depends(get_db)):

    db_todo = db.query(models.Todo).filter(models.Todo.username == user.username).\
        filter(models.Todo.todo_id == todo_id).first()
    if db_todo is None:
        raise HTTPException(
            status_code=404,
            detail=f"Item number {todo_id} was not found"
        )
    db.delete(db_todo)
    db.commit()
    return


# Update completion of existing to do
@router.patch("/{todo_id}", response_model=ShowTodo)
async def update_todo_completion(todo_id: int,
                                 completed: bool = True,
                                 user: UserIn = Depends(get_current_user),
                                 db: Session = Depends(get_db)):

    db_todo = db.query(models.Todo).filter(models.Todo.username == user.username).\
        filter(models.Todo.todo_id == todo_id)
    if db_todo is None:
        raise HTTPException(
            status_code=404,
            detail=f"Item number {todo_id} was not found"
        )
    db_todo.update({'completion': completed})
    db.commit()
    return db_todo.first()
