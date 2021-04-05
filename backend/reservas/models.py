from django.db import models

from equipamentos.models import Equipamento


class Reserva(models.Model):
    """Recorda que um equipamento está reservado em determinada data"""

    equipamento = models.ForeignKey(
        Equipamento, related_name='reservas', on_delete=models.CASCADE
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def __repr__(self):
        return f'<Reserva: {self.equipamento.name}' + \
            ' ({self.start_date.date}-{self.end_date.date})>'
