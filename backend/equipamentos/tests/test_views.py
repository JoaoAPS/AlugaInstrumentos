from rest_framework import status
from mixer.backend.django import mixer
from datetime import date

from equipamentos.models import Equipamento
from equipamentos.serializers import EquipamentoSerializer
from categorias.models import Categoria
from reservas.models import Reserva


def test_equipamento_list_view_basic(list_url, userClient):
    """Testa a list view dos equipamentos sem GET params"""
    mixer.blend(Equipamento)
    mixer.blend(Equipamento)
    mixer.blend(Equipamento)

    equipamentos = Equipamento.objects.all().order_by('name')
    serializer = EquipamentoSerializer(equipamentos, many=True)
    res = userClient.get(list_url)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data


def test_equipamento_list_view_optional_params(list_url, userClient):
    """Testa a list view dos equipamentos com GET params sort e categorias"""
    c1 = mixer.blend(Categoria)
    c2 = mixer.blend(Categoria)

    e1 = mixer.blend(
        Equipamento, name='e1', categorias=[c1, c2], price_per_day=1.0
    )
    e2 = mixer.blend(
        Equipamento, name='e2', categorias=[c2], price_per_day=5.0
    )
    mixer.blend(Equipamento, categorias=[c1])

    res = userClient.get(list_url + f'?categorias={c2.id}&sort=-price_per_day')
    equipamentos = [e2, e1]
    serializer = EquipamentoSerializer(equipamentos, many=True)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data


def test_equipamento_list_view_filter_available_dates(list_url, userClient):
    """Testa lista de equipamentos filtrada pelo dia que estão disponíveis"""
    e1 = mixer.blend(Equipamento)
    e2 = mixer.blend(Equipamento)
    e3 = mixer.blend(Equipamento)

    e1.reservas.set([])
    e2.reservas.set([])
    e3.reservas.set([])
    mixer.blend(
        Reserva,
        equipamento=e1,
        start_date=date(2021, 1, 5),
        end_date=date(2021, 1, 8)
    )
    mixer.blend(
        Reserva,
        equipamento=e2,
        start_date=date(2021, 1, 9),
        end_date=date(2021, 1, 12)
    )
    mixer.blend(
        Reserva,
        equipamento=e3,
        start_date=date(2021, 1, 11),
        end_date=date(2021, 1, 15)
    )

    serializer = EquipamentoSerializer([e3], many=True)
    res = userClient.get(
        list_url + '?start_date=2021-01-02&end_date=2021-01-10'
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data


def test_equipamento_retrieve_view_successful(
    detail_url, userClient, equipamento
):
    """Testa que a retrieve view dos equipamentos retorna os dados corretos"""
    res = userClient.get(detail_url(equipamento.id))
    serializer = EquipamentoSerializer(equipamento)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data


def test_equipamento_retrieve_view_unexisting_id(detail_url, userClient):
    """Testa a retrieve view dos equipamentos para um id que não existe"""
    res = userClient.get(detail_url(999))
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_equipamento_create_view_mandatory_parameters_only(
    list_url, adminClient
):
    """Testa api de criação de equipamento com apenas os params obrigatórios"""
    payload = {'name': 'New equip', 'price_per_day': 4.99}
    res = adminClient.post(list_url, payload)

    assert res.status_code == status.HTTP_201_CREATED
    assert Equipamento.objects.filter(**payload).exists()


def test_equipamento_create_view_all_parameters(list_url, adminClient):
    """Testa api de criação de equipamento passando parâmetros opcionais"""
    cat = mixer.blend(Categoria)
    payload = {
        'name': 'New equip',
        'price_per_day': 4.99,
        'description': 'Lorem Ipsum dolor sit amet',
        'categorias': [cat.id]
    }
    res = adminClient.post(list_url, payload)
    payload.pop('categorias')
    equip = Equipamento.objects.filter(**payload)

    assert res.status_code == status.HTTP_201_CREATED
    assert equip.exists()
    assert cat in equip.first().categorias.all()


def test_equipamento_create_view_missing_mandatory_parameter(
    list_url, adminClient
):
    """Testa create view de equipamentos quando falta parâmetro obrigatório"""
    res = adminClient.post(list_url, {'name': 'Nome'})
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert len(Equipamento.objects.all()) == 0


def test_equipamento_full_update_view_successful(
    detail_url, adminClient, equipamento
):
    """Testa modificação de equipamento pela api"""
    cat = mixer.blend(Categoria)
    payload = {
        'name': 'New name',
        'price_per_day': 4.99,
        'description': 'Lorem Ipsum dolor sit amet',
        'categorias': [cat.id]
    }

    res = adminClient.put(detail_url(equipamento.id), payload)
    equipamento.refresh_from_db()

    assert res.status_code == status.HTTP_200_OK
    assert equipamento.name == payload['name']
    assert float(equipamento.price_per_day) == payload['price_per_day']
    assert equipamento.description == payload['description']
    assert cat in equipamento.categorias.all()


def test_equipamento_full_update_view_missing_mandatory_parameter(
    detail_url, adminClient, equipamento
):
    """Testa modificação de equipamento pela api quando falta um parâmetro"""
    payload = {'price_per_day': 4.99, 'description': 'Lorem sit amet'}

    res = adminClient.put(detail_url(equipamento.id), payload)
    equipamento.refresh_from_db()

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert equipamento.price_per_day != payload['price_per_day']


def test_equipamento_partial_update_view_successful(
    detail_url, adminClient, equipamento
):
    """Testa modificação parcial de equipamento pela api"""
    payload = {'price_per_day': 43.99}
    res = adminClient.patch(detail_url(equipamento.id), payload)
    equipamento.refresh_from_db()

    assert res.status_code == status.HTTP_200_OK
    assert float(equipamento.price_per_day) == payload['price_per_day']


def test_equipamento_update_view_unexisting_id(detail_url, adminClient):
    """Testa que tentar modificar um equipamento que não existe falha"""
    res = adminClient.put(detail_url(77), {'name': 'N', 'price_per_day': 1.4})
    assert res.status_code == status.HTTP_404_NOT_FOUND

    res = adminClient.patch(detail_url(7), {'name': 'N', 'price_per_day': 1.4})
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_equipamento_delete_view_successful(
    detail_url, adminClient, equipamento
):
    """Testa deleção de equipamentos pela api"""
    res = adminClient.delete(detail_url(equipamento.id))
    assert res.status_code == status.HTTP_204_NO_CONTENT
    assert not Equipamento.objects.filter(id=equipamento.id).exists()


def test_equipamento_delete_view_unexisting_id(detail_url, adminClient):
    """Testa que tentar deletar um equipamento que não existe falha"""
    res = adminClient.delete(detail_url(2412))
    assert res.status_code == status.HTTP_404_NOT_FOUND
