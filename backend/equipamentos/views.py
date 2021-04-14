from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from equipamentos.models import Equipamento
from equipamentos.serializers import EquipamentoSerializer
from categorias.models import Categoria
from core.utils import iso_to_date


class EquipamentoViewSet(ModelViewSet):
    """Viewset do model Equipamento"""

    queryset = Equipamento.objects.all()
    serializer_class = EquipamentoSerializer

    def get_permissions(self):
        """Apenas admins podem modificar equipamentos"""
        permission_classes = [permissions.AllowAny] \
            if self.action in ['list', 'retrieve'] \
            else [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Aplica filtros dos parâmetros GET"""
        queryset = super().get_queryset()

        # Filtra os que estão disponíveis em determinada data
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date or end_date:
            id_valids = [
                equip.id for equip in queryset
                if equip.isAvailableAt(
                    start_date=iso_to_date(start_date),
                    end_date=iso_to_date(end_date)
                )
            ]
            queryset = queryset.filter(id__in=id_valids)

        # Filtra instrumentos
        is_instrument = self.request.query_params.get('instrumento')
        if is_instrument is not None:
            is_instrument = bool(is_instrument)
            queryset = queryset.filter(is_instrument=is_instrument)

        # Filtra por categorias
        categoria_ids = self.request.query_params.get('categorias')
        if categoria_ids:
            categoria_ids = map(int, categoria_ids.split(','))
            categorias = Categoria.objects.filter(id__in=categoria_ids)
            queryset = queryset.filter(categorias__in=categorias).distinct()

        # Ordanação
        sort_field = self.request.query_params.get('sort', 'name')
        queryset = queryset.order_by(sort_field)

        return queryset
