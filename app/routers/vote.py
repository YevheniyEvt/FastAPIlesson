from fastapi import  status, HTTPException, APIRouter, Depends
from sqlmodel import select
from typing import Annotated

from .. import oauth2
from ..schemas import VotePublic
from ..models import User, Vote, Post
from ..database import SessionDep


router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: VotePublic, session: SessionDep,
         current_user: Annotated[User, Depends(oauth2.get_current_user)]):

    post = session.get(Post, vote.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {vote.post_id} does not exist")

    found_vote = session.exec(select(Vote).where(Vote.post_id == vote.post_id,
                                                 Vote.user_id == current_user.id)).first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already vted post {vote.post_id}")
        new_vote = Vote(post_id = vote.post_id, user_id=current_user.id)
        db_vote = Vote.model_validate(new_vote)
        session.add(db_vote)
        session.commit()
        return {"message": "successfully added vote"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Vote does not exist")
        session.delete(found_vote)
        session.commit()

        return {"message": "successfully deleted vote"}