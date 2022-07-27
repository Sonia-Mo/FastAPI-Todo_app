from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
import models
from authentication import get_password_hash, get_current_user
from database import get_db
from routers.users.schemas import UserIn, UserOut

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


# Get all users
@router.get("/", response_model=list[UserOut])
async def get_all_users(user: UserIn = Depends(get_current_user),
                        db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    if user.username == 'admin':
        return db.query(models.User).offset(skip).limit(limit).all()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Regular user is not permitted to this list"
        )


# Get single user
@router.get("/{username}", response_model=UserOut)
async def get_user(user: UserIn = Depends(get_current_user)):
    return user


# Create new user
@router.post("/", response_model=UserOut)
async def create_user(new_user: UserIn, db: Session = Depends(get_db)):
    username_exists = db.query(models.User).filter(models.User.username == new_user.username).first()
    if username_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Choose another username"
        )
    email_exists = db.query(models.User).filter(models.User.email == new_user.email).first()
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"email already exists"
        )

    hashed_password = get_password_hash(new_user.password)
    db_user = models.User(username=new_user.username,
                          email=new_user.email,
                          hashed_password=hashed_password,
                          todo_count=0
                          )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Delete user
@router.delete("/{username}")
async def delete_user(user: UserIn = Depends(get_current_user), db: Session = Depends(get_db)):
    db.delete(user)
    db.commit()
