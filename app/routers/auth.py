import datetime

from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlmodel import select
from typing import Annotated
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from .. import utils, oauth2
from  ..models import User
from ..schemas import Token
from ..database import SessionDep

router = APIRouter(tags=['Authetication'])

@router.post('/login', response_model=Token)
def login_for_access_token(
        user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: SessionDep):

    user = session.exec(select(User).where(User.email == user_credentials.username)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")

    if not utils.verify(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")

    access_token = oauth2.create_access_token(data={'user_id': user.id})

    return {'access_token': access_token,  'token_type': 'bearer'}

