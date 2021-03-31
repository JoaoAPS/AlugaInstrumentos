from django.db import models
from django.contrib.auth import get_user_model

from kits.models import Kit


class Pedido(models.Model):
    """Um pedido de aluguel de um kit por um usuário"""

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='pedidos'
    )
    kit = models.ForeignKey(
        Kit, on_delete=models.PROTECT, related_name='pedidos'
    )
    start_date = models.DateField()
    end_date = models.DateField()

    @property
    def days_rented(self):
        """Retorna o número de dias que o kit ficará alugado"""
        return (self.end_date - self.start_date).days

    @property
    def price(self):
        """Retorna o preço total do aluguel do kit pelos dias requisitados"""
        return self.days_rented() * self.kit.price_per_day()

    def __str__(self):
        return f'<Pedido {self.id} - {self.user.email}>'

    __repr__ = __str__
