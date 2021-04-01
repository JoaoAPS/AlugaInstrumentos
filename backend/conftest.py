import pytest
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model


@pytest.fixture
def user(db):
    """Retorna um objeto user não administrador"""
    return get_user_model().objects.create_user(
        email='user@mail.com',
        name='Test User',
        password='testpass'
    )


@pytest.fixture
def admin(db):
    """Retorna um objeto user administrador"""
    return get_user_model().objects.create_superuser(
        email='admin@mail.com',
        name='Test Admin User',
        password='testpass'
    )


@pytest.fixture
def unauthenticatedClient():
    """Retorna um api client sem ninguém autenticado"""
    return APIClient()


@pytest.fixture
def userClient(user):
    """Retorna um api client autenticado com um user normal"""
    client = APIClient()
    client.force_authenticate(user)
    return client


@pytest.fixture
def adminClient(admin):
    """Retorna um api client autenticado com um user administrador"""
    client = APIClient()
    client.force_authenticate(admin)
    return client
