from django.contrib.auth import get_user_model
from rest_framework import status
from mixer.backend.django import mixer
from datetime import date

from pedidos.models import Pedido
from pedidos.serializers import PedidoSerializer
from equipamentos.models import Equipamento
from reservas.models import Reserva
from core import services


# --- List ---
def test_pedido_list_view_only_shows_user_pedidos(userClient, user, list_url):
    """Testa que a listagem de pedidos só mostra os do usuário logado"""
    user2 = mixer.blend(get_user_model())
    p1 = mixer.blend(Pedido, user=user)
    p2 = mixer.blend(Pedido, user=user)
    mixer.blend(Pedido, user=user2)

    res = userClient.get(list_url)
    serializer = PedidoSerializer([p1, p2], many=True)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data


# --- Detail ---
def test_pedido_retrieve_view_successful(
    userClient, pedido, detail_url, userFactory
):
    """Testa pedido retrieve view retorna os dados do pedido"""
    res = userClient.get(detail_url(pedido.id))
    serializer = PedidoSerializer(
        pedido, context={'request': userFactory.get(detail_url(pedido.id))}
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data


def test_pedido_retrieve_view_unexisting_pedido(userClient, detail_url):
    """Testa pedido retrieve view de um pedido que não existe gera um erro"""
    res = userClient.get(detail_url(124))
    assert res.status_code == status.HTTP_404_NOT_FOUND


# --- Create ---
def test_pedido_create_view_required_parameters_only(userClient, list_url):
    """Testa criação de pedido pela api passando apenas valores obrigatórios"""
    e1 = mixer.blend(Equipamento)
    e2 = mixer.blend(Equipamento)
    res = userClient.post(list_url, {'equipamentos': [e1.id, e2.id]})

    assert res.status_code == status.HTTP_201_CREATED

    pedido = Pedido.objects.get(id=res.data['id'])
    assert e1 in pedido.equipamentos.all()
    assert e2 in pedido.equipamentos.all()


def test_pedido_create_view_all_parameters(userClient, list_url):
    """Testa criação de pedido pela api passando todos valores disponíveis"""
    e1 = mixer.blend(Equipamento)
    e2 = mixer.blend(Equipamento)
    payload = {
        'equipamentos': [e1.id, e2.id],
        'start_date': date(2021, 2, 14),
        'end_date': date(2021, 2, 26)
    }

    res = userClient.post(list_url, payload)

    assert res.status_code == status.HTTP_201_CREATED

    pedido = Pedido.objects.get(id=res.data['id'])
    assert e1 in pedido.equipamentos.all()
    assert e2 in pedido.equipamentos.all()
    assert pedido.start_date == payload['start_date']
    assert pedido.end_date == payload['end_date']


def test_pedido_create_view_missing_required_parameter(userClient, list_url):
    """Testa pedido não é criado quando falta um parâmetro obrigatório"""
    res = userClient.post(list_url, {'start_date': date(2000, 6, 6)})

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert Pedido.objects.count() == 0


def test_pedido_create_view_invalid_date_payload(userClient, list_url):
    """Testa que end_date deve sempre ser depois de start_date"""
    e = mixer.blend(Equipamento)
    payload = {
        'equipamentos': [e.id],
        'start_date': date(2021, 5, 1),
        'end_date': date(2021, 4, 1),
    }
    res = userClient.post(list_url, payload)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert Pedido.objects.count() == 0


def test_pedido_create_view_invalid_payload(userClient, list_url):
    """Testa create view quando os algum equipamento é inválido"""
    res = userClient.post(list_url, {'equipamentos': [55]})

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert Pedido.objects.count() == 0


# --- Update ---
def test_pedido_update_view_successful(userClient, detail_url, pedido):
    """Testa modificação de pedido pela api"""
    payload = {'start_date': date(2023, 2, 14), 'end_date': date(2026, 1, 3)}
    res = userClient.patch(detail_url(pedido.id), payload)
    pedido.refresh_from_db()

    assert res.status_code == status.HTTP_200_OK
    assert pedido.start_date == payload['start_date']
    assert pedido.end_date == payload['end_date']


def test_pedido_update_view_unexisting_pedido(userClient, detail_url):
    """Testa modificação de um pedido que não existe gera um erro"""
    res = userClient.patch(detail_url(881), {'start_date': date(2026, 2, 14)})
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_pedido_update_view_invalid_date_payload(
    userClient, detail_url, pedido
):
    """Testa que end_date deve sempre ser depois de start_date"""
    payload = {'start_date': date(2021, 5, 1), 'end_date': date(2021, 4, 1)}
    res = userClient.patch(detail_url(pedido.id), payload)
    pedido.refresh_from_db()

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert pedido.start_date < pedido.end_date


# --- Delete ---
def test_pedido_delete_view_successful(userClient, detail_url, pedido):
    """Testa deleção de um pedido pela api"""
    res = userClient.delete(detail_url(pedido.id))

    assert res.status_code == status.HTTP_204_NO_CONTENT
    assert not Pedido.objects.filter(id=pedido.id).exists()


def test_pedido_delete_view_executed_pedido(userClient, detail_url, pedido):
    """Testa que tentar deletar pela api um pedido em execução gera um erro"""
    services.executePedido(pedido)
    res = userClient.delete(detail_url(pedido.id))

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert Pedido.objects.filter(id=pedido.id).exists()


def test_pedido_delete_view_unexisting_pedido(userClient, detail_url):
    """Testa que tentar deletar um pedido que não existe gera um erro"""
    res = userClient.delete(detail_url(467))
    assert res.status_code == status.HTTP_404_NOT_FOUND


# --- Add Item ---
def test_pedido_add_item_view_successful(userClient, add_item_url, pedido):
    """Testa adição de um equipamento em um pedido pela api"""
    equip = mixer.blend(Equipamento)
    res = userClient.post(add_item_url(pedido.id), {'equipamento': equip.id})
    pedido.refresh_from_db()

    assert res.status_code == status.HTTP_200_OK
    assert equip in pedido.equipamentos.all()


def test_pedido_add_item_view_invalid_equipamento(
    userClient, add_item_url, pedido
):
    """Testa adição de equipamento no pedido gera erro se aquele não existe"""
    res = userClient.post(add_item_url(pedido.id), {'equipamento': 124})
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_pedido_add_item_view_unexisting_pedido(userClient, detail_url):
    """Testa adição de equipamento em um pedido que não existe gera um erro"""
    equip = mixer.blend(Equipamento)
    res = userClient.post(412, {'equipamento': equip.id})
    assert res.status_code == status.HTTP_404_NOT_FOUND


# --- Remove Item ---
def test_pedido_remove_item_view_successful(
    userClient, remove_item_url, pedido
):
    """Testa remoção de um equipamento de um pedido pela api"""
    equip = mixer.blend(Equipamento)
    pedido.equipamentos.add(equip)
    pedido.save()

    res = userClient.delete(remove_item_url(pedido.id, equip.id))
    pedido.refresh_from_db()

    assert res.status_code == status.HTTP_204_NO_CONTENT
    assert equip not in pedido.equipamentos.all()


def test_pedido_remove_item_view_unexisting_equipamento(
    userClient, remove_item_url, pedido
):
    """Testa que remover um equipamento que não está no pedido gera erro"""
    res = userClient.delete(remove_item_url(pedido.id, 421))
    assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_pedido_remove_item_view_unexisting_pedido(
    userClient, remove_item_url
):
    """Testa que remover equipamento de um pedido que não existe gera erro"""
    equip = mixer.blend(Equipamento)
    res = userClient.delete(remove_item_url(421, equip.id))
    assert res.status_code == status.HTTP_404_NOT_FOUND


# --- Confirmation ---
def test_pedido_confirmation_view_successful(
    userClient, confirmation_url, pedido
):
    """Testa confirmação e execução de um pedido pela api"""
    equip = mixer.blend(Equipamento)
    pedido.equipamentos.add(equip)

    res = userClient.post(confirmation_url(pedido.id))
    pedido.refresh_from_db()

    assert res.status_code == status.HTTP_200_OK
    assert pedido.executed
    assert Reserva.objects.filter(
        equipamento=equip,
        pedido=pedido,
        start_date=pedido.start_date,
        end_date=pedido.end_date,
    ).exists()


def test_pedido_confirmation_view_already_confirmed(
    userClient, confirmation_url, pedido
):
    """Testa que não é possível executar o mesmo pedido mais de uma vez"""
    userClient.post(confirmation_url(pedido.id))
    res = userClient.post(confirmation_url(pedido.id))
    assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_pedido_confirmation_invalid_pedido(
    userClient, confirmation_url, pedido
):
    """Testa que não se confirma um pedido com equipamentos indisponíveis"""
    equip = mixer.blend(Equipamento)
    pedido.equipamentos.add(equip)
    mixer.blend(
        Reserva,
        equipamento=equip,
        start_date=date(2021, 3, 20),
        end_date=date(2021, 4, 20),
    )
    pedido.start_date = date(2021, 4, 1)
    pedido.end_date = date(2021, 4, 3)
    pedido.save()

    res = userClient.post(confirmation_url(pedido.id))
    pedido.refresh_from_db()

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert not pedido.executed


def test_pedido_confirmation_view_unexisting_pedido(
    userClient, confirmation_url
):
    """Testa que tentar executar um pedido que não existe gera erro"""
    res = userClient.post(confirmation_url(213))
    assert res.status_code == status.HTTP_404_NOT_FOUND


# --- Cancelation ---
def test_pedido_cancelation_view_successful(
    userClient, cancelation_url, pedido
):
    """Testa cancelamento de um pedido em execução"""
    services.executePedido(pedido)
    res = userClient.post(cancelation_url(pedido.id))
    pedido.refresh_from_db()

    assert res.status_code == status.HTTP_204_NO_CONTENT
    assert not pedido.executed


def test_pedido_cancelation_view_unconfirmed_pedido(
    userClient, cancelation_url, pedido
):
    """Testa que tentar cancelar um pedido que não foi executado gera erro"""
    res = userClient.post(cancelation_url(pedido.id))
    assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_pedido_cancelation_view_unexisting_pedido(
    userClient, cancelation_url
):
    """Testa que tentar cancelar um pedido que não existe gera erro"""
    res = userClient.post(cancelation_url(42))
    assert res.status_code == status.HTTP_404_NOT_FOUND
