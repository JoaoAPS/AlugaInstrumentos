from django.db import models
from django.contrib.auth import get_user_model

from equipamentos.models import Equipamento


class Pedido(models.Model):
    """Um pedido de aluguel de equipamentos por um usuário"""

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='pedidos'
    )
    equipamentos = models.ManyToManyField(Equipamento, related_name='pedidos')
    start_date = models.DateField(null=True, default=None)
    end_date = models.DateField(null=True, default=None)
    executed = models.BooleanField(default=False)

    @property
    def days_rented(self):
        """Retorna o número de dias que o kit ficará alugado"""
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None

    @property
    def price_per_day(self):
        """Retorna o preço total de um dia do aluguel"""
        return sum(equip.price_per_day for equip in self.equipamentos)

    @property
    def price(self):
        """
        Retorna o preço total do aluguel dos equipamentos pelos dias
        requisitados
        """
        return self.days_rented() * self.price_per_day()

    def __str__(self):
        return f'<Pedido {self.id} - {self.user.email}>'

    __repr__ = __str__
