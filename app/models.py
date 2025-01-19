from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, DateTime

from .schemas import PostBase, UserBase
from datetime import datetime


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field()
    created_at: datetime = Field(default=datetime.now(),
                                 sa_column=Column(DateTime(timezone=True), nullable=False))

    posts: list["Post"] = Relationship(back_populates='user', cascade_delete=True)


class Post(PostBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.now(),
                                 sa_column=Column(DateTime(timezone=True), nullable=False))

    owner_id: int = Field(foreign_key="user.id", ondelete="CASCADE")
    user: User = Relationship(back_populates='posts')

class Vote(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", ondelete="CASCADE", primary_key=True)
    post_id: int = Field(foreign_key="post.id", ondelete="CASCADE", primary_key=True)

