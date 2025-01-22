from fastapi import Response, status, HTTPException, APIRouter, Depends
from sqlmodel import select
from typing import Annotated

from .. import utils, oauth2
from ..schemas import UserUpdate, UserCreate, UserPublic
from ..models import User
from ..database import SessionDep

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

def check_user_not_in_db(user: UserCreate, session: SessionDep):
    find_user = session.exec(select(User).where(User.email == user.email)).first()
    if find_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with email: {user.email} already registered")

    return user


def check_user_in_db(id: int, session: SessionDep):
    db_user = session.get(User, id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")
    return id


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserPublic )
def create_user(user: Annotated[UserCreate, Depends(check_user_not_in_db)], session: SessionDep):

    hashed_password = utils.hash(user.password)
    extra_data = {"hashed_password": hashed_password}
    db_user = User.model_validate(user, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/", response_model=list[UserPublic])
def get_users(session: SessionDep):
    user = session.exec(select(User)).all()
    return user


@router.get("/{id}", response_model=UserPublic)
def get_user(id: int, session: SessionDep):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not found")
    return user

@router.put("/{id}", response_model=UserPublic)
def update_user(id: int,
                user: UserUpdate,
                session: SessionDep,
                ):

    db_user = session.get(User, id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")
    db_user = session.get(User, id)
    user_data = user.model_dump(exclude_unset=True)
    extra_data = {}
    if 'password' in user_data:
        password = user_data['password']
        hashed_password = utils.hash(password)
        extra_data['hashed_password'] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, session: SessionDep):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")
    session.delete(user)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)