import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app import schemas, models, oauth2


@pytest.mark.parametrize('title, content, published, status_code', [
    ("test post", 'content of test post', True, 201),
    ("test post2", 'content of test post2', False, 201),
])
def test_create_post(auth_client: TestClient, session: Session,
                     title, content, published, status_code):
    response = auth_client.post('posts/',
                           json={'title': title, 'content': content, 'published': published})
    data = response.json()
    post = schemas.PostPublic(**data)

    assert post.title == title
    assert post.content == content
    assert post.published == published
    assert response.status_code == status_code


@pytest.mark.parametrize('title, content, published, status_code', [
    ("test post", 'content of test post', True, 401),
    ("test post2", 'content of test post2', False, 401),
])
def test_not_auth_user_create_post(client: TestClient,
                       title, content, published, status_code):
    response = client.post('posts/',
                           json={'title': title, 'content': content, 'published': published})

    assert response.status_code == status_code


def test_create_post_without_published(auth_client: TestClient, session: Session,):
    response = auth_client.post('posts/',
                           json={'title': "title post", 'content': "content post",})

    assert response.status_code == 201

def test_create_post_without_content(auth_client: TestClient, session: Session,):
    response = auth_client.post('posts/',
                           json={'title': "title post", "published": True})

    assert response.status_code == 422

def test_create_post_without_title(auth_client: TestClient, session: Session,):
    response = auth_client.post('posts/',
                           json={'content': "content post", "published": True})

    assert response.status_code == 422


def test_get_posts(create_posts, auth_client: TestClient, session: Session):
    response = auth_client.get('posts/',
                          params={'limit': 3, 'skip': 2, 'search': 'post'})
    data = response.json()

    id_post_3 = session.exec(select(models.Post).offset(2)).first().id
    post_data = schemas.PostWithVote(**data[0])
    assert len(data) == 3
    assert post_data.post.id == id_post_3
    assert "post" in post_data.post.title
    assert response.status_code == 200


def test_not_auth_user_get_posts(client: TestClient):
    response = client.get('posts/')
    assert response.status_code == 401


def test_get_posts_without_param(create_posts, auth_client: TestClient, session: Session):
    response = auth_client.get('posts/')
    data = response.json()
    assert len(data) > 0
    assert response.status_code == 200


@pytest.mark.parametrize('id_post, status_code', [
    (i, 200) for i in range(1,2)
])
def test_get_post(create_posts, auth_client: TestClient, id_post, status_code):
    response = auth_client.get(f'posts/{id_post}')
    post = schemas.PostWithVote(**response.json())
    assert post.post.id == id_post
    assert response.status_code == status_code


@pytest.mark.parametrize('id_post, status_code', [
    (i, 404) for i in range(20,22)
])
def test_get_wrong_post(create_posts, auth_client: TestClient, id_post, status_code):
    response = auth_client.get(f'posts/{id_post}')
    assert response.status_code == status_code


@pytest.mark.parametrize('id_post, status_code', [
    (i, 401) for i in range(1,2)
])
def test_not_auth_user_get_post(client: TestClient, id_post, status_code):
    response = client.get(f'posts/{id_post}')
    assert response.status_code == status_code


@pytest.mark.parametrize('id_post, title, content, published, status_code', [
    (1, 'some', 'some cont', False, 200),
    (3, 'some', 'some cont', False, 200),
])
def test_update_post(create_posts, auth_client: TestClient,
                     id_post, title, content, published, status_code):

    response = auth_client.put(f'posts/{id_post}',
                               json={'title': title, 'content': content, 'published':published })
    data = response.json()
    post = schemas.PostPublic(**data)

    assert post.id == id_post
    assert post.title == title
    assert post.content == content
    assert post.published == published
    assert response.status_code == status_code


@pytest.mark.parametrize('id_post, title, content, published, status_code', [
    (1, 'some', 'some cont', False, 403),
    (3, 'some', 'some cont', False, 403),
    (5, 'some', 'some cont', False, 403),
])
def test_update_not_user_post(create_posts, create_users, client: TestClient,
                              id_post, title, content, published, status_code):
    access_token = oauth2.create_access_token(data={'user_id': 2})
    response = client.put(f'posts/{id_post}',
                             json={'title': title, 'content': content, 'published':published },
                             headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == status_code


@pytest.mark.parametrize('id_post, status_cod', [
    (1, 204),
    (2, 204),
])
def test_delete_post(create_posts, auth_client: TestClient,
                     id_post, status_cod):
    response = auth_client.delete(f'posts/{id_post}')
    assert response.status_code == status_cod


@pytest.mark.parametrize('id_post, status_cod', [
    (111, 404),
    (2111, 404),
])
def test_delete_wrong_post(create_posts, auth_client: TestClient,
                     id_post, status_cod):
    response = auth_client.delete(f'posts/{id_post}')
    assert response.status_code == status_cod


@pytest.mark.parametrize('id_post, status_cod', [
    (1, 403),
    (2, 403),
])
def test_delete_not_user_post(create_posts, create_users, client: TestClient,
                     id_post, status_cod):
    access_token = oauth2.create_access_token(data={'user_id': 2})
    response = client.delete(f'posts/{id_post}',
                                  headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == status_cod




