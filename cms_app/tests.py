import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import Author, Post, Like


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return Author.objects.create_user(email='hardeep@gmail.com', password='harryahmedabad')

@pytest.fixture
def auth_token(user):
    token, created = Token.objects.get_or_create(user=user)
    return token

@pytest.fixture
def authenticated_client(api_client, auth_token):
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + auth_token.key)
    return api_client

@pytest.mark.django_db
def test_author_create(api_client):
    url = reverse('user-create')
    data = {
        'username': 'Hardeep96',
        'email': 'hardeep@gmail.com',
        'password': 'harryahmedabad'
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert Author.objects.filter(email='hardeep@gmail.com').exists()
    assert response.data == {'id':1,'email':'hardeep@gmail.com'}


@pytest.mark.django_db
def test_author_login(api_client, auth_token):
    url = reverse('user-login')
    data = {
        'email': 'hardeep@gmail.com',
        'password': 'harryahmedabad'
    }
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert response.data['token'] == auth_token.key


@pytest.mark.django_db
def test_author_update(authenticated_client, user):
    url = reverse('user-update-delete')
    data = {
        'username': 'Mukesh18',
        'first_name': 'Mukesh',
        'last_name': 'Patel',
        'email': 'mukeshp@gmail.com'
    }
    response = authenticated_client.put(url, data)
    assert response.status_code == 200
    assert 'Mukesh18' in response.data['username'] and user.email in response.data['email']


@pytest.mark.django_db
def test_blog_create(authenticated_client, user):
    url = reverse('blog-create-getall')
    post_obj = Post.objects.create(author=user, title='Test Post', description='Test Description', content='Test Content is available here', is_public=True)
    data = {
        'title': 'Test Post',
        'description': 'Test Description',
        'content': 'Test Content is available here',
        'is_public': True
    }
    response = authenticated_client.post(url, data)
    assert response.status_code == 201
    assert post_obj.title == response.data['title']


@pytest.mark.django_db
def test_blog_update(authenticated_client, user):
    post_obj = Post.objects.create(author=user, title='Testing Post2', description='Test Description again', content='Test Content is no more here now', is_public=False)
    data = {
        'title': 'Test Post',
        'description': 'Test Description',
        'content': 'Test Content is available here',
        'is_public': True
    }
    url = reverse('blog-get-put-delete', args=[post_obj.id])
    response = authenticated_client.get(url, data)
    assert response.status_code == 200
    assert post_obj.content == response.data['content']


@pytest.mark.django_db
def test_like_blog(authenticated_client, user):
    post_obj = Post.objects.create(author=user, title='Test Post', description='Test Description', content='Test Content', is_public=True)
    url = reverse('like-unlike-blog', args=[post_obj.id])
    response = authenticated_client.post(url)
    assert response.status_code == 201

@pytest.mark.django_db
def test_unlike_blog(authenticated_client, user):
    post_obj = Post.objects.create(author=user, title='Test Post', description='Test Description', content='Test Content', is_public=False)
    like = Like.objects.create(author=user, post=post_obj)
    url = reverse('like-unlike-blog', args=[post_obj.id])
    response = authenticated_client.delete(url)
    assert response.status_code == 204
