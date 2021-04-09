import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
def test_auth_token_view_successful():
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
    get_user_model().objects.create_user(
        email='test@mm.com', name='Testo', password='123test'
    )

    url = reverse('auth-token')
    res = APIClient().post(
        url, {'username': 'test@mm.com', 'password': 'wrong_pass'}
    )

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert 'token' not in res.data.keys()
