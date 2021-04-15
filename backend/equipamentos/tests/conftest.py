import pytest
from django.urls import reverse

from equipamentos.models import Equipamento
from categorias.models import Categoria


@pytest.fixture
def list_url():
    return reverse('equipamento-list')


@pytest.fixture
def detail_url():
    def get_url(equip_id):
        return reverse('equipamento-detail', args=[equip_id])
    return get_url


@pytest.fixture
def equipamento(db, tmp_image):
    cat = Categoria.objects.create(name='Test Cat', is_instrument=True)
    equip = Equipamento.objects.create(
        title='Test Equip',
        description='lorem ipsum',
        price_per_day=1.00,
        is_instrument=True,
        image=tmp_image.name
    )
    equip.categorias.add(cat)
    return equip
