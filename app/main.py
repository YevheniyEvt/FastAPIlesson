from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from .routers import post, user, auth, vote
from .database import create_db_and_tables

create = 0


@asynccontextmanager
async def lifespan(app: FastAPI):
    if create:
        create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

origins = ["http://localhost",
           "http://localhost:8080",
           "http://127.0.0.1:8000",
           "https://www.google.com",
           "https://www.youtube.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}







