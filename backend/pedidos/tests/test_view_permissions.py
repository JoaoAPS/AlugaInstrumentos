from rest_framework import status
from mixer.backend.django import mixer

from pedidos.models import Pedido
from equipamentos.models import Equipamento


def test_pedido_list_view_permissions(
    unauthenticatedClient, userClient, adminClient, list_url
):
    """Testa as permissões na list view da api dos pedidos"""
    res = unauthenticatedClient.get(list_url)
    assert res.status_code == status.HTTP_403_FORBIDDEN

    res = userClient.get(list_url)
    assert res.status_code == status.HTTP_200_OK

    res = adminClient.get(list_url)
    assert res.status_code == status.HTTP_200_OK


def test_pedido_retrieve_view_permissions(
    unauthenticatedClient, userClient, adminClient, detail_url, user, admin
):
    """Testa as permissões na retrieve view da api dos pedidos"""
    res = unauthenticatedClient.get(detail_url(0))
    assert res.status_code == status.HTTP_403_FORBIDDEN

    pedido = mixer.blend(Pedido, user=user)
    res = userClient.get(detail_url(pedido.id))
    assert res.status_code == status.HTTP_200_OK

    pedido = mixer.blend(Pedido, user=admin)
    res = adminClient.get(detail_url(pedido.id))
    assert res.status_code == status.HTTP_200_OK

    # Pedidos de outros usuários
    res = userClient.get(detail_url(pedido.id))
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_pedido_create_view_permissions(
    unauthenticatedClient, userClient, adminClient, list_url
):
    """Testa as permissões na create view da api dos pedidos"""
    equipamento = mixer.blend(Equipamento)
    payload = {'equipamentos': [equipamento.id]}

    res = unauthenticatedClient.post(list_url, payload)
    assert res.status_code == status.HTTP_403_FORBIDDEN

    res = userClient.post(list_url, payload)
    assert res.status_code != status.HTTP_403_FORBIDDEN

    res = adminClient.post(list_url, payload)
    assert res.status_code != status.HTTP_403_FORBIDDEN


def test_pedido_update_view_permissions(
    unauthenticatedClient, userClient, adminClient, detail_url, user, admin
):
    """Testa as permissões na update view da api dos pedidos"""
    payload = {'equipamentos': []}

    res = unauthenticatedClient.patch(detail_url(0), payload)
    assert res.status_code == status.HTTP_403_FORBIDDEN

    pedido = mixer.blend(Pedido, user=user)
    res = userClient.patch(detail_url(pedido.id), payload)
    assert res.status_code == status.HTTP_200_OK

    pedido = mixer.blend(Pedido, user=admin)
    res = adminClient.patch(detail_url(pedido.id), payload)
    assert res.status_code == status.HTTP_200_OK

    # Pedidos de outros usuários
    res = userClient.patch(detail_url(pedido.id), payload)
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_pedido_delete_view_permissions(
    unauthenticatedClient, userClient, adminClient, detail_url, user, admin
):
    """Testa as permissões na delete view da api dos pedidos"""
    res = unauthenticatedClient.delete(detail_url(0))
    assert res.status_code == status.HTTP_403_FORBIDDEN

    pedido = mixer.blend(Pedido, user=user)
    res = userClient.delete(detail_url(pedido.id))
    assert res.status_code == status.HTTP_204_NO_CONTENT

    pedido = mixer.blend(Pedido, user=admin)
    res = adminClient.delete(detail_url(pedido.id))
    assert res.status_code == status.HTTP_204_NO_CONTENT

    # Pedidos de outros usuários
    res = userClient.delete(detail_url(pedido.id))
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_pedido_add_item_view_permissions(
    unauthenticatedClient, userClient, adminClient, add_item_url, user, admin
):
    """Testa as permissões na add_item view da api dos pedidos"""
    equipamento = mixer.blend(Equipamento)
    payload = {'equipamento': equipamento.id}

    res = unauthenticatedClient.post(add_item_url(0), payload)
    assert res.status_code == status.HTTP_403_FORBIDDEN

    pedido = mixer.blend(Pedido, user=user)
    res = userClient.post(add_item_url(pedido.id), payload)
    assert res.status_code == status.HTTP_200_OK

    pedido = mixer.blend(Pedido, user=admin)
    res = adminClient.post(add_item_url(pedido.id), payload)
    assert res.status_code == status.HTTP_200_OK

    # Pedidos de outros usuários
    res = userClient.post(add_item_url(pedido.id), payload)
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_pedido_remove_item_view_permissions(
    unauthenticatedClient,
    userClient,
    adminClient,
    remove_item_url,
    user,
    admin
):
    """Testa as permissões na remove_item view da api dos pedidos"""
    equipamento = mixer.blend(Equipamento)

    res = unauthenticatedClient.delete(remove_item_url(0, 0))
    assert res.status_code == status.HTTP_403_FORBIDDEN

    pedido = mixer.blend(Pedido, user=user)
    pedido.equipamentos.add(equipamento)
    res = userClient.delete(remove_item_url(pedido.id, equipamento.id))
    assert res.status_code == status.HTTP_204_NO_CONTENT

    pedido = mixer.blend(Pedido, user=admin)
    pedido.equipamentos.add(equipamento)
    res = adminClient.delete(remove_item_url(pedido.id, equipamento.id))
    assert res.status_code == status.HTTP_204_NO_CONTENT

    # Pedidos de outros usuários
    res = userClient.delete(remove_item_url(pedido.id, equipamento.id))
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_pedido_confirmation_view_permissions(
    unauthenticatedClient,
    userClient,
    adminClient,
    confirmation_url,
    user,
    admin
):
    """Testa as permissões na confirmation view da api dos pedidos"""
    res = unauthenticatedClient.post(confirmation_url(0))
    assert res.status_code == status.HTTP_403_FORBIDDEN

    pedido = mixer.blend(Pedido, user=user)
    res = userClient.post(confirmation_url(pedido.id))
    assert res.status_code != status.HTTP_403_FORBIDDEN

    pedido = mixer.blend(Pedido, user=admin)
    res = adminClient.post(confirmation_url(pedido.id))
    assert res.status_code != status.HTTP_403_FORBIDDEN

    # Pedidos de outros usuários
    res = userClient.post(confirmation_url(pedido.id))
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_pedido_cancelation_view_permissions(
    unauthenticatedClient,
    userClient,
    adminClient,
    cancelation_url,
    user,
    admin
):
    """Testa as permissões na cancelation view da api dos pedidos"""
    res = unauthenticatedClient.post(cancelation_url(0))
    assert res.status_code == status.HTTP_403_FORBIDDEN

    pedido = mixer.blend(Pedido, user=user)
    res = userClient.post(cancelation_url(pedido.id))
    assert res.status_code != status.HTTP_403_FORBIDDEN

    pedido = mixer.blend(Pedido, user=admin)
    res = adminClient.post(cancelation_url(pedido.id))
    assert res.status_code != status.HTTP_403_FORBIDDEN

    # Pedidos de outros usuários
    res = userClient.post(cancelation_url(pedido.id))
    assert res.status_code == status.HTTP_404_NOT_FOUND
