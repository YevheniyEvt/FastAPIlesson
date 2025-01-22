import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
import datetime

from app import schemas, models
from app.oauth2 import get_current_user



def test_root(client: TestClient):
    response  = client.get("/")
    assert response .json().get("message") == "Hello World"
    assert response .status_code == 200


def test_create_user(client: TestClient):
    response  = client.post(
        '/users/', json={'email': 'email3@mail.com', 'password': 'password'},
    )
    data = response.json()
    new_user = schemas.UserPublic(**data)
    assert new_user.email == 'email3@mail.com'
    assert new_user.id > 0

    assert response.status_code == 201


@pytest.mark.parametrize('wrong_id, status_cod', [
    (10, 404),
    (30, 404),
    (40, 404),
])
def test_check_user_in_db(create_users ,client: TestClient,
                          wrong_id, status_cod):
    response = client.get(f'users/{wrong_id}')
    assert response.status_code == status_cod


@pytest.mark.parametrize('email, password, status_cod', [
    ('email3@mail.com', 'password1234', 200),
    ('email4@mail.com', 'password1234', 200),
])
def test_login(create_users, client: TestClient, session: Session,
               email, password, status_cod):
    response = client.post(
        'login/', data={'username': email, 'password': password}
    )

    data = schemas.Token(**response.json())
    user = get_current_user(data.access_token, session)
    assert user.email == email
    assert data.token_type == 'bearer'
    assert response.status_code == status_cod


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongMail@mail.com', 'password1234', 401),
    ('email3@mail.com', 'wrongPassword', 401),
    ('wrongMail@mail.com', 'wrongPassword', 401),
    (None, 'wrongPassword', 401),
    ('wrongMail@mail.com', None, 401),
])
def test_wrong_login(create_users, client: TestClient,
                     email, password, status_code):
    response = client.post(
        'login/', data={'username': email, 'password': password}
    )
    assert response.status_code == status_code


def test_get_users(create_users, client: TestClient, session: Session):
    response = client.get('users/')
    data = response.json()
    for i, _ in enumerate(data):
        user = schemas.UserPublic(**data[i])
        assert user.id
        assert user.email
        assert user.created_at
        assert response.status_code == 200




def test_no_users_get(client: TestClient):
    response = client.get('users/')
    data = response.json()
    assert data == []


@pytest.mark.parametrize('user_id, email, status_cod', [
    (1, 'email3@mail.com', 200),
    (2,'email4@mail.com', 200),
])
def test_get_user(create_users, client: TestClient,
                  user_id, email, status_cod):
    response = client.get(f'users/{user_id}')
    data = response.json()
    user = schemas.UserPublic(**data)
    assert response.status_code == status_cod
    assert user.email == email
    assert user.id == user_id
    assert user.created_at.strftime('%m/%d/%Y') == datetime.date.today().strftime('%m/%d/%Y')
    assert user.created_at.strftime('%m/%d/%Y') == datetime.date.today().strftime('%m/%d/%Y')


@pytest.mark.parametrize('user_id, email, password, status_cod', [
    (1, '11email3@mail.com', 'password12311', 200),
    (2,'12email4@mail.com', 'password1234234', 200),
])
def test_update_user(create_users, client: TestClient, session: Session,
                     user_id, email, password, status_cod):
    response = client.put(f'users/{user_id}', json={'email': email, 'password': password})

    data = response.json()
    update_user = schemas.UserPublic(**data)
    assert update_user.email == email
    assert update_user.id == user_id
    assert response .status_code == status_cod


@pytest.mark.parametrize('user_id, status_cod', [
    (1, 204),
    (2, 204),
])
def test_delete_user(create_users, client: TestClient,
                     user_id, status_cod):
    response = client.delete(f'users/{user_id}')
    assert response.status_code == status_cod



