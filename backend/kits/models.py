from django.db import models
from django.contrib.auth import get_user_model

from equipamentos.models import Equipamento


class Kit(models.Model):
    """Um kit com equipamentos para serem alugados em conjunto"""

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    equipamentos = models.ManyToManyField(Equipamento, related_name='kits')

    @property
    def price_per_day(self):
        return sum(equip.price_per_day for equip in self.equipamentos)
