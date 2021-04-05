from django.db import models

from equipamentos.models import Equipamento
from pedidos.models import Pedido


class Reserva(models.Model):
    """Recorda que um equipamento está reservado em determinada data"""

    pedido = models.ForeignKey(
        Pedido, related_name='reservas', on_delete=models.CASCADE
    )
    equipamento = models.ForeignKey(
        Equipamento, related_name='reservas', on_delete=models.CASCADE
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def __repr__(self):
        return f'<Reserva: {self.equipamento.name}' + \
            ' ({self.start_date.date}-{self.end_date.date})>'
