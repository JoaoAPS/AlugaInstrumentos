import pytest
from django.urls import reverse
from mixer.backend.django import mixer
from datetime import date

from pedidos.models import Pedido
from equipamentos.models import Equipamento


@pytest.fixture
def pedido(user):
    pedido = Pedido.objects.create(
        user=user, start_date=date(2021, 1, 1), end_date=date(2021, 1, 5)
    )
    pedido.equipamentos.add(mixer.blend(Equipamento))
    return pedido


@pytest.fixture
def list_url():
    return reverse('pedido-list')


@pytest.fixture
def detail_url():
    def get_url(pedido_id):
        return reverse('pedido-detail', args=[pedido_id])
    return get_url


@pytest.fixture
def add_item_url():
    def get_url(pedido_id):
        return reverse('pedido-add_item', args=[pedido_id])
    return get_url


@pytest.fixture
def remove_item_url():
    def get_url(pedido_id, equip_id):
        return reverse('pedido-remove_item', args=[pedido_id, equip_id])
    return get_url


@pytest.fixture
def confirmation_url():
    def get_url(pedido_id):
        return reverse('pedido-confirmation', args=[pedido_id])
    return get_url


@pytest.fixture
def cancelation_url():
    def get_url(pedido_id):
        return reverse('pedido-cancelation', args=[pedido_id])
    return get_url
