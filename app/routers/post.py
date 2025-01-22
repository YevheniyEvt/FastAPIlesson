
from fastapi import Response, status, HTTPException, APIRouter, Depends, Path, Query
from sqlmodel import select, col
from typing import Annotated
from sqlalchemy import func


from .. import oauth2
from ..schemas import PostUpdate, PostCreate, PostPublic, PostWithVote
from ..models import Post, User, Vote
from ..database import SessionDep

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostPublic)
def create_posts(post: PostCreate, session: SessionDep,
                 current_user: Annotated[User, Depends(oauth2.get_current_user)]):
    extra_data = {"owner_id": current_user.id}
    db_post = Post.model_validate(post, update=extra_data)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@router.get("/",response_model=list[PostWithVote])
def get_posts(session: SessionDep,
                 current_user: Annotated[User, Depends(oauth2.get_current_user)],
            search: Annotated[str, Query()] ='',
             limit: Annotated[int | None, Query()]=5,
              skip: Annotated[int | None, Query()]=0
              ):

    #posts = session.exec(select(Post).where(col(Post.title).contains(search)).offset(skip).limit(limit)).all()
    statement = select(
        Post,
        func.count(Vote.post_id).label("votes"),
    ).where(col(Post.title).contains(search))

    results = session.exec(statement.join(
        Vote,
        isouter=True,
    ).offset(skip).limit(limit).group_by(Post.id)).all()

    #return posts
    return [{"post": post, "votes": vote} for post, vote in results]


@router.get("/{id}", response_model=PostWithVote)
def get_post(id: Annotated[int, Path()], session: SessionDep,
                 current_user: Annotated[User, Depends(oauth2.get_current_user)]):

    statement  = select(
        Post,
        func.count(Vote.post_id).label("votes"),
    ).where(Post.id == id)

    post = session.exec(statement.join(
        Vote,
        isouter=True,
    ).group_by(Post.id)).first()

    #post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post": post[0], "votes": post[1]}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, session: SessionDep,
                 current_user: Annotated[User, Depends(oauth2.get_current_user)]):
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")
    session.delete(post)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=PostPublic)
def update_post(id:int, post: PostUpdate, session: SessionDep,
                 current_user: Annotated[User, Depends(oauth2.get_current_user)]):
    db_post = session.get(Post, id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")

    post_data = post.model_dump(exclude_unset=True)
    db_post.sqlmodel_update(post_data)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post