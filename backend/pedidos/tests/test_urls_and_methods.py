import pytest
from django.urls import reverse
from rest_framework import status
from mixer.backend.django import mixer

from pedidos.models import Pedido
from equipamentos.models import Equipamento


@pytest.mark.parametrize('view_name,url', [
    ('pedido-list', '/api/pedidos/'),
    ('pedido-detail', '/api/pedidos/1/'),
    ('pedido-add_item', '/api/pedidos/1/'),
    ('pedido-remove_item', '/api/pedidos/1/equipamentos/2/'),
    ('pedido-confirmation', '/api/pedidos/1/confirmation/'),
    ('pedido-cancelation', '/api/pedidos/1/cancelation/'),
])
def test_pedidos_view_urls(view_name, url):
    """Testa que os urls da api de pedidos são mapeados corretamente"""
    args = [] if view_name == 'pedido-list' else [1]
    if view_name == 'pedido-remove_item':
        args.append(2)

    assert reverse(view_name, args=args) == url


@pytest.mark.parametrize('method,allowed', [
    ('get', True),
    ('post', True),
    ('put', False),
    ('patch', False),
    ('delete', False),
])
def test_pedido_set_allowed_methods(method, allowed, adminClient, list_url):
    """Testa os métodos permitidos da view de conjunto dos pedidos"""
    res = getattr(adminClient, method)(list_url)
    assert (res.status_code != status.HTTP_405_METHOD_NOT_ALLOWED) == allowed


@pytest.mark.parametrize('method,allowed', [
    ('get', True),
    ('post', True),
    ('put', False),
    ('patch', True),
    ('delete', True),
])
def test_pedido_detail_allowed_methods(
    method, allowed, adminClient, detail_url
):
    """Testa os métodos permitidos da view de conjunto dos pedidos"""
    pedido = mixer.blend(Pedido)
    res = getattr(adminClient, method)(detail_url(pedido.id))
    assert (res.status_code != status.HTTP_405_METHOD_NOT_ALLOWED) == allowed


@pytest.mark.parametrize('method,allowed', [
    ('get', False),
    ('post', False),
    ('put', False),
    ('patch', False),
    ('delete', True),
])
def test_pedido_remove_item_allowed_methods(
    method, allowed, adminClient, remove_item_url
):
    """Testa os métodos permitidos da view de conjunto dos pedidos"""
    pedido = mixer.blend(Pedido)
    equipamento = mixer.blend(Equipamento)
    pedido.equipamentos.add(equipamento)
    res = getattr(adminClient, method)(
        remove_item_url(pedido.id, equipamento.id)
    )

    assert (res.status_code != status.HTTP_405_METHOD_NOT_ALLOWED) == allowed


@pytest.mark.parametrize('method,allowed', [
    ('get', False),
    ('post', True),
    ('put', False),
    ('patch', False),
    ('delete', False),
])
def test_pedido_confirmation_allowed_methods(
    method, allowed, adminClient, confirmation_url
):
    """Testa os métodos permitidos da view de conjunto dos pedidos"""
    pedido = mixer.blend(Pedido)
    res = getattr(adminClient, method)(confirmation_url(pedido.id))
    assert (res.status_code != status.HTTP_405_METHOD_NOT_ALLOWED) == allowed


@pytest.mark.parametrize('method,allowed', [
    ('get', False),
    ('post', True),
    ('put', False),
    ('patch', False),
    ('delete', False),
])
def test_pedido_cancelation_allowed_methods(
    method, allowed, adminClient, cancelation_url
):
    """Testa os métodos permitidos da view de conjunto dos pedidos"""
    pedido = mixer.blend(Pedido)
    res = getattr(adminClient, method)(cancelation_url(pedido.id))
    assert (res.status_code != status.HTTP_405_METHOD_NOT_ALLOWED) == allowed
