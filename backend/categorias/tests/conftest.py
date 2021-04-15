import pytest
from django.urls import reverse

from categorias.models import Categoria


@pytest.fixture
def categoria(db):
    return Categoria.objects.create(name='categoria teste', is_instrument=True)


@pytest.fixture
def categorias_list_url():
    return reverse('categoria-list')


@pytest.fixture
def categorias_detail_url():
    def get_detail_url(id):
        return reverse('categoria-detail', args=[id])
    return get_detail_url
