import pytest
from rest_framework import status
from mixer.backend.django import mixer

from equipamentos.models import Equipamento


def test_equipamento_list_api_permissions(
    unauthenticatedClient, userClient, adminClient, list_url
):
    """Testa que a list view dos equipamentos tem as permissões corretas"""
    res = unauthenticatedClient.get(list_url)
    assert res.status_code == status.HTTP_200_OK

    res = userClient.get(list_url)
    assert res.status_code == status.HTTP_200_OK

    res = adminClient.get(list_url)
    assert res.status_code == status.HTTP_200_OK


def test_equipamento_retrieve_api_permissions(
    unauthenticatedClient, userClient, adminClient, detail_url
):
    """Testa que a retrieve view dos equipamentos tem as permissões corretas"""
    equip = mixer.blend(Equipamento)

    res = unauthenticatedClient.get(detail_url(equip.id))
    assert res.status_code == status.HTTP_200_OK

    res = userClient.get(detail_url(equip.id))
    assert res.status_code == status.HTTP_200_OK

    res = adminClient.get(detail_url(equip.id))
    assert res.status_code == status.HTTP_200_OK


def test_equipamento_create_api_permissions(
    unauthenticatedClient, userClient, adminClient, list_url
):
    """Testa que a create view dos equipamentos tem as permissões corretas"""
    payload = {'title': 'Test equip', 'price_per_day': 10.0}

    res = unauthenticatedClient.post(list_url, payload)
    assert res.status_code == status.HTTP_403_FORBIDDEN

    res = userClient.post(list_url, payload)
    assert res.status_code == status.HTTP_403_FORBIDDEN

    res = adminClient.post(list_url, payload)
    assert res.status_code != status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize('method', ['put', 'patch'])
def test_equipamento_update_api_permissions(
    method, unauthenticatedClient, userClient, adminClient, detail_url
):
    """Testa que a update view dos equipamentos tem as permissões corretas"""
    equip = mixer.blend(Equipamento, title='Primeiro nome')
    payload = {'title': 'Outro nome', 'price_per_day': 10.0}

    res = getattr(unauthenticatedClient, method)(detail_url(equip.id), payload)
    assert res.status_code == status.HTTP_403_FORBIDDEN

    res = getattr(userClient, method)(detail_url(equip.id), payload)
    assert res.status_code == status.HTTP_403_FORBIDDEN

    res = getattr(adminClient, method)(detail_url(equip.id), payload)
    assert res.status_code != status.HTTP_403_FORBIDDEN


def test_equipamento_delete_api_permissions(
    unauthenticatedClient, userClient, adminClient, detail_url
):
    """Testa que a delete view dos equipamentos tem as permissões corretas"""
    equip = mixer.blend(Equipamento)

    res = unauthenticatedClient.delete(detail_url(equip.id))
    assert res.status_code == status.HTTP_403_FORBIDDEN

    res = userClient.delete(detail_url(equip.id))
    assert res.status_code == status.HTTP_403_FORBIDDEN

    res = adminClient.delete(detail_url(equip.id))
    assert res.status_code == status.HTTP_204_NO_CONTENT
