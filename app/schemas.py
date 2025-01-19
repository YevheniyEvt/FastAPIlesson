from sqlmodel import SQLModel, Field
from pydantic import EmailStr, conint
from datetime import datetime





class UserBase(SQLModel):
    email: EmailStr = Field(unique=True)


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    email: EmailStr | None = None
    password: str | None = None


class UserPublic(UserBase):
    id: int
    created_at: datetime

class UserLogin(UserBase):
    email: EmailStr
    password: str

#----------------------------------------------------

class PostBase(SQLModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    ...


class PostUpdate(PostBase):
    title: str | None = None
    content: str | None = None
    published: bool | None = None


class PostPublic(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    user: UserPublic
    #votes : int

class PostWithVote(SQLModel):
    post: PostPublic
    votes: int



#--------------------------------------------------

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    id: int | None = None


#------------------------

class VotePublic(SQLModel):
    post_id: int
    dir: conint(le=1)