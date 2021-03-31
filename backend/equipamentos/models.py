from django.db import models

from categorias.models import Categoria


class Equipamento(models.Model):
    """Um equipamento que pode ser alugado pelo cliente"""

    name = models.CharField('nome', max_length=255)
    description = models.TextField('descrição')
    price_per_day = models.DecimalField(
        'preço por dia', decimal_places=2, max_digits=10
    )
    categorias = models.ManyToManyField(Categoria, related_name='equipamentos')

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Equipamento: ' + str(self) + '>'
