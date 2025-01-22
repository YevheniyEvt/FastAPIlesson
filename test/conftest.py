import pytest
import datetime
import random
from sqlmodel.pool import StaticPool
from fastapi.testclient import TestClient

from sqlmodel import Session, SQLModel, create_engine, select
from app.main import app
from app.database import get_session
from app import utils, models, oauth2, schemas


@pytest.fixture(name='session')
def session_fixture():
    engine = create_engine(
        'sqlite://',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name='client')
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name='create_users')
def create_teste_users(session: Session):
    user1 = models.User(
        email='email3@mail.com', id=1, created_at = datetime.date.today(),
        hashed_password=utils.hash('password1234'))
    user2 = models.User(
        email='email4@mail.com', id=2, created_at = datetime.date.today(),
        hashed_password=utils.hash('password1234'))
    session.add(user1)
    session.add(user2)
    session.commit()


@pytest.fixture(name='create_token')
def create_current_user_token(create_users, session):
    access_token = oauth2.create_access_token(data={'user_id': 1})
    return access_token

@pytest.fixture(name='create_posts')
def create_test_posts(session: Session):
    for i in range(10):
        post = models.Post(
            title=f'title post #{i}',
            content=f'content of post #{i}',
            published=random.choice([1,0]),
            owner_id=1
        )
        session.add(post)
        session.commit()

@pytest.fixture(name='auth_client')
def create_auth_client(client: TestClient, create_token):
    client.headers = {**client.headers,
                      'Authorization': f'Bearer {create_token}'}
    return client


@pytest.fixture(name='votes')
def create_vote(client: TestClient, session: Session):
    for i in range(4):
        vote = models.Vote(post_id=i, user_id=1)
        session.add(vote)
        session.commit()
