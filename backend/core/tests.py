import pytest
from mixer.backend.django import mixer
from datetime import date

from core.services import executePedido, cancelPedido
from pedidos.models import Pedido
from reservas.models import Reserva
from equipamentos.models import Equipamento
from core.exceptions import EquipamentoUnavailable, DuplicateExecution


# --- Set up ---
@pytest.fixture
def equip1():
    return mixer.blend(Equipamento)


@pytest.fixture
def equip2():
    return mixer.blend(Equipamento)


@pytest.fixture
def pedido(user, equip1, equip2):
    pedido = Pedido.objects.create(
        user=user, start_date=date(2021, 3, 1), end_date=date(2021, 3, 5)
    )
    pedido.equipamentos.add(equip1)
    pedido.equipamentos.add(equip2)
    return pedido


# --- executePedido ---
def test_executePedido_successful(pedido, equip1, equip2):
    """Testa que executePedido cria reservas e muda status do pedido"""
    executePedido(pedido)

    assert pedido.executed
    assert Reserva.objects.filter(
        pedido=pedido,
        equipamento=equip1,
        start_date=date(2021, 3, 1),
        end_date=date(2021, 3, 5)
    ).exists()
    assert Reserva.objects.filter(
        pedido=pedido,
        equipamento=equip2,
        start_date=date(2021, 3, 1),
        end_date=date(2021, 3, 5)
    ).exists()


def test_executePedido_invalid_dates(user, equip1):
    """Testa que executePedido falha se as datas estão inválidas"""
    # Sem end_date
    pedido = Pedido.objects.create(user=user, start_date=date(2021, 3, 1))
    with pytest.raises(ValueError):
        executePedido(pedido)

    # Sem start_date
    pedido = Pedido.objects.create(user=user, end_date=date(2021, 3, 5))
    with pytest.raises(ValueError):
        executePedido(pedido)


def test_executePedido_unavailable_equipamento(pedido, equip1):
    """Testa que executePedido falha se algum equipamento está indisponível"""
    Reserva.objects.create(
        pedido=pedido,
        equipamento=equip1,
        start_date=date(2021, 3, 2),
        end_date=date(2021, 3, 4),
    )

    with pytest.raises(EquipamentoUnavailable):
        executePedido(pedido)


def test_executePedido_already_executed(pedido):
    """Testa que executePedido falha se o pedido já foi executado antes"""
    executePedido(pedido)
    
    with pytest.raises(DuplicateExecution):
        executePedido(pedido)


# --- cancelPedido ---
def test_cancelPedido_successful(pedido, equip1, equip2):
    """Testa que cancelPedido remove reservas e volta status do pedido"""
    executePedido(pedido)
    cancelPedido(pedido)

    assert not pedido.executed
    assert not Reserva.objects.filter(
        pedido=pedido,
        equipamento=equip1,
        start_date=date(2021, 3, 1),
        end_date=date(2021, 3, 5)
    ).exists()
    assert not Reserva.objects.filter(
        pedido=pedido,
        equipamento=equip2,
        start_date=date(2021, 3, 1),
        end_date=date(2021, 3, 5)
    ).exists()
    assert pedido.reservas.count() == 0


def test_cancelPedido_not_yet_executed(pedido):
    """Testa que cancelPedido falha se o pedido não foi executado antes"""
    with pytest.raises(DuplicateExecution):
        cancelPedido(pedido)
