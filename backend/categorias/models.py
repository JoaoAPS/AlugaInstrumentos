from django.db import models


class Categoria(models.Model):
    """Categoria que um equipamento pode ter"""

    name = models.CharField('nome', max_length=64)
    is_instrument = models.BooleanField()

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Categoria: " + str(self) + '>'
