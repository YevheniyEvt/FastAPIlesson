import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from urllib3 import proxy_from_url

from app import schemas, models, oauth2


@pytest.mark.parametrize('post_id, message, status_code', [
    (6, 'successfully added vote', 201),
    (7, 'successfully added vote', 201),
    (8, 'successfully added vote', 201),
])
def test_add_vote(create_posts, votes, auth_client: TestClient,
                  post_id, message, status_code):
    response = auth_client.post('/vote',
                                json={'post_id': post_id, 'dir': 1})
    data = response.json()

    assert data.get('message') == message
    assert response.status_code == status_code


@pytest.mark.parametrize('post_id, message, status_code', [
    (1, 'successfully deleted vote', 201),
    (2, 'successfully deleted vote', 201),
    (3, 'successfully deleted vote', 201),
])
def test_del_vote(create_posts, votes, auth_client: TestClient,
                  post_id, message, status_code):
    response = auth_client.post('/vote',
                                json={'post_id': post_id, 'dir': 0})
    data = response.json()

    assert data.get('message') == message
    assert response.status_code == status_code


@pytest.mark.parametrize('post_id, message, status_code', [
    (1, 'successfully deleted vote', 409),
    (2, 'successfully deleted vote', 409),
    (3, 'successfully deleted vote', 409),
])
def test_add_vote_twice(create_posts, votes, auth_client: TestClient,
                  post_id, message, status_code):
    response = auth_client.post('/vote',
                                json={'post_id': post_id, 'dir': 1})
    data = response.json()
    assert response.status_code == status_code


@pytest.mark.parametrize('post_id, message, status_code', [
    (6, 'Vote does not exist', 404),
    (7, 'Vote does not exist', 404),
    (8, 'Vote does not exist', 404),
])
def test_del_vote_twice(create_posts, votes, auth_client: TestClient,
                  post_id, message, status_code):
    response = auth_client.post('/vote',
                                json={'post_id': post_id, 'dir': 0})
    data = response.json()
    assert data['detail'] == message
    assert response.status_code == status_code


def test_delete_vote_non_exist(create_posts, votes, auth_client: TestClient):
    response = auth_client.post('/vote',
                                json={'post_id': 123, 'dir': 0})
    assert response.status_code == 404


def test_vote_non_exist(create_posts, votes, auth_client: TestClient):
    response = auth_client.post('/vote',
                                json={'post_id': 123, 'dir': 1})
    assert response.status_code == 404

def test_not_auth_user_vote_post(client: TestClient):
    response = client.post('/vote',
                                json={'post_id': 6, 'dir': 1})
    assert response.status_code == 401