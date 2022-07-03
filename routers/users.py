from fastapi import APIRouter, HTTPException
from models import UserIn, UserOut

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

memory: list[UserIn] = []


# Get all users
@router.get("/", response_model=list[UserOut])
async def get_all_users():
    return memory


# Get single user
@router.get("/{username}", response_model=UserOut)
async def get_user(username: str):
    for elem in memory:
        if elem.username == username:
            return elem
    raise HTTPException(
        status_code=404,
        detail=f"User with username '{username}' was not found"
    )


# Create new user
@router.post("/", response_model=UserOut)
async def create_user(new_user: UserIn):
    memory.append(new_user)
    return new_user


# Delete to do
@router.delete("/{username}")
async def delete_user(username: str):
    for elem in memory:
        if elem.username == username:
            memory.remove(elem)
            return
    raise HTTPException(
        status_code=404,
        detail=f"User with username '{username}' was not found"
    )
