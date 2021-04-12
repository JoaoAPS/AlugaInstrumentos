import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


def test_auth_token_view_url():
    """Testa que o url da auth_token_view está mapeado corretamente"""
    assert reverse('auth-token') == '/api/registration/login/'


@pytest.mark.django_db
def test_auth_token_view_successful():
    """Testa que auth_token_view retorna token para credenciais corretas"""
    user = get_user_model().objects.create_user(
        email='test@mm.com', name='Testo', password='123test'
    )

    url = reverse('auth-token')
    res = APIClient().post(
        url, {'username': 'test@mm.com', 'password': '123test'}
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data['email'] == user.email
    assert res.data['id'] == user.id
    assert 'token' in res.data.keys()


@pytest.mark.django_db
def test_auth_token_view_unsuccessful():
    """Testa que auth_token_view retorna erro para credenciais incorretas"""
    get_user_model().objects.create_user(
        email='test@mm.com', name='Testo', password='123test'
    )

    url = reverse('auth-token')
    res = APIClient().post(
        url, {'username': 'test@mm.com', 'password': 'wrong_pass'}
    )

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert 'token' not in res.data.keys()


def test_user_register_view_url():
    """Testa que o url da user_register_view está mapeado corretamente"""
    assert reverse('user-register') == '/api/registration/register/'


@pytest.mark.django_db
def test_user_register_view_successful():
    """Testa que user_register_view cria usuário e retorna token"""
    url = reverse('user-register')
    payload = {
        'email': 'new@gotmail.com',
        'name': 'New user',
        'password1': 'my_great_password',
        'password2': 'my_great_password'
    }
    res = APIClient().post(url, payload)

    assert res.status_code == status.HTTP_200_OK
    assert res.data['email'] == payload['email']
    assert 'token' in res.data.keys()
    assert get_user_model().objects.filter(
        email=payload['email'], name=payload['name']
    ).exists()


@pytest.mark.django_db
def test_user_register_view_missing_field():
    """Testa que user_register_view retorna erro se falta algum campo"""
    url = reverse('user-register')
    payload = {
        'email': 'new@gotmail.com',
        'password1': 'my_great_password',
        'password2': 'my_great_password'
    }
    res = APIClient().post(url, payload)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert 'token' not in res.data.keys()


@pytest.mark.django_db
def test_user_register_view_password_error():
    """Testa que user_register_view retorna erro se há problema nas senhas"""
    url = reverse('user-register')
    payload = {
        'email': 'new@gotmail.com',
        'name': 'New user',
        'password1': 'my_great_password',
        'password2': 'not_same_password'
    }
    res = APIClient().post(url, payload)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert type(res.data) != dict or 'token' not in res.data.keys()
