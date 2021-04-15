import pytest
from rest_framework.test import APIClient, \
                                APIRequestFactory, \
                                force_authenticate
from PIL import Image
import tempfile
import os

from django.contrib.auth import get_user_model
from django.conf import settings


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


@pytest.fixture
def factory():
    return APIRequestFactory()


@pytest.fixture
def userFactory(user):
    f = APIRequestFactory()
    force_authenticate(f, user=user)
    return f


@pytest.fixture
def tmp_image():
    file = tempfile.NamedTemporaryFile(suffix='.png')
    image = Image.new('RGB', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.seek(0)
    yield file

    file.close()
    if os.path.isfile(
        os.path.join(settings.MEDIA_ROOT, 'equipaments', file.path)
    ):
        os.remove(os.path.join(settings.MEDIA_ROOT, 'equipaments', file.path))

