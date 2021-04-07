from pedidos.models import Pedido
from reservas.models import Reserva
from core.exceptions import EquipamentoUnavailable, DuplicateExecution


def executePedido(pedido: Pedido):
    """Confirma o pedido no sistema e começa seu processamento"""
    if pedido.executed:
        raise DuplicateExecution('Esse pedido já foi executado!')

    # Corfirma que a data do aluguel está definida
    if pedido.start_date is None or pedido.end_date is None:
        raise ValueError(
            'A data de início e término do aluguel devem ser especificadas'
        )

    reservas = []

    for equipamento in pedido.equipamentos.all():
        # Checa se o equipamento está disponível
        if not equipamento.isAvailableAt(
            start_date=pedido.start_date, end_date=pedido.end_date
        ):
            raise EquipamentoUnavailable(
                f'{equipamento.name} (id {equipamento.id}) não está ' +
                'disponível entre {pedido.start_date} e {pedido.end_date}.'
            )

        # Prepara a reserva
        reservas.append(Reserva(
            pedido=pedido,
            equipamento=equipamento,
            start_date=pedido.start_date,
            end_date=pedido.end_date
        ))

    # Executa as reservas
    for reserva in reservas:
        reserva.save()
        pedido.reservas.add(reserva)

    pedido.executed = True
    pedido.save()


def cancelPedido(pedido: Pedido):
    """Cancela um pedido que está sendo executado"""
    if not pedido.executed:
        raise DuplicateExecution(
            'O pedido não pode ser cancelado pois não está sendo executado!'
        )

    for reserva in pedido.reservas.all():
        reserva.delete()

    pedido.executed = False
    pedido.save()
