from django.db import models

from categorias.models import Categoria


class Equipamento(models.Model):
    """Um equipamento que pode ser alugado pelo cliente"""

    name = models.CharField('nome', max_length=255)
    description = models.TextField('descrição', blank=True)
    price_per_day = models.DecimalField(
        'preço por dia', decimal_places=2, max_digits=10
    )
    image = models.ImageField(upload_to='equipaments')
    is_instrument = models.BooleanField()
    categorias = models.ManyToManyField(
        Categoria, related_name='equipamentos', blank=True
    )

    def isAvailableAt(self, start_date=None, end_date=None):
        """Retorna se o equipamento pode ser alugado nesse período"""

        # Checa erro de argumento
        if not start_date and not end_date:
            raise ValueError('Ao menos um entre start_date e end_date deve' +
                ' ser passado para checar se o equipamento está disponível!')            

        if start_date is not None:
            # Checa se a start_date está no meio de uma reserva
            for reserva in self.reservas.filter(start_date__lte=start_date):
                if reserva.end_date >= start_date:
                    return False

            if end_date is not None:
                if end_date < start_date:
                    raise ValueError('A data de término da reversa deve ser' +
                        'depois da data de início dela!')

                # Checa se alguma reserva inicia no meio do período desejado
                if self.reservas.filter(
                    start_date__gte=start_date, start_date__lte=end_date
                ).exists():
                    return False

        # Se apenas a end_date foi passada
        else:
            # Checa se a end_date está no meio de uma reserva
            for reserva in self.reservas.filter(start_date__lte=end_date):
                if reserva.end_date >= end_date:
                    return False

        return True

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Equipamento: ' + str(self) + '>'
